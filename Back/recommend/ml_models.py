import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
from django.conf import settings
import os
from products.models import DepositProducts, SavingProducts, MortgageProducts

class UserBasedRecommender:
    def __init__(self):
        self.model_path = os.path.join(settings.BASE_DIR, 'recommendations', 'ml_models')
        self.scaler = None
        self.models = {
            'deposit': None,
            'saving': None,
            'mortgage': None
        }
        self._load_or_train_models()

    def _load_or_train_models(self):
        """모델 로드 또는 훈련"""
        try:
            self.scaler = joblib.load(os.path.join(self.model_path, 'scaler.pkl'))
            for product_type in self.models.keys():
                model_file = os.path.join(self.model_path, f'{product_type}_model.pkl')
                self.models[product_type] = joblib.load(model_file)
        except:
            self._train_models()

    def _prepare_user_features(self, user):
        """사용자 특성 벡터 생성"""
        age = (pd.Timestamp.now() - pd.Timestamp(user.birthdate)).days // 365
        
        # 소득 수준 계산 (1-10)
        income_level = min(user.annual_income // 10000000, 10)
        
        # 자산 수준 계산 (1-10)
        asset_level = min(user.assets // 100000000, 10)
        
        # 투자성향 수치화
        risk_scores = {
            'CONSERVATIVE': 1,
            'MODERATE': 2,
            'AGGRESSIVE': 3,
            'SPECULATIVE': 4
        }
        risk_score = risk_scores[user.investment_type]
        
        features = [
            age,
            income_level,
            asset_level,
            risk_score
        ]
        
        return np.array(features).reshape(1, -1)

    def _train_models(self):
        """모델 훈련"""
        self.scaler = StandardScaler()
        
        # 각 상품 유형별 모델 훈련
        for product_type in self.models.keys():
            X_train, y_train = self._generate_dummy_data(product_type)
            X_scaled = self.scaler.fit_transform(X_train)
            
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
            model.fit(X_scaled, y_train)
            self.models[product_type] = model
            
            # 모델 저장
            if not os.path.exists(self.model_path):
                os.makedirs(self.model_path)
                
            joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.pkl'))
            joblib.dump(
                model, 
                os.path.join(self.model_path, f'{product_type}_model.pkl')
            )

    def _generate_dummy_data(self, product_type, n_samples=1000000):
        """더미 데이터 생성"""
        np.random.seed(42)
        
        # 특성 생성
        ages = np.random.normal(40, 10, n_samples).clip(20, 80)
        income_levels = np.random.randint(1, 11, n_samples)
        asset_levels = np.random.randint(1, 11, n_samples)
        risk_scores = np.random.randint(1, 5, n_samples)
        
        X = np.column_stack([ages, income_levels, asset_levels, risk_scores])
        
        # 상품 ID 가져오기
        if product_type == 'deposit':
            products = DepositProducts.objects.all()
        elif product_type == 'saving':
            products = SavingProducts.objects.all()
        else:
            products = MortgageProducts.objects.all()
            
        product_ids = [p.id for p in products]
        
        if not product_ids:
            raise ValueError(f"No {product_type} products found in database")
        
        # 규칙 기반 더미 데이터 생성
        y = []
        for i in range(n_samples):
            age = ages[i]
            income = income_levels[i]
            assets = asset_levels[i]
            risk = risk_scores[i]
            
            # 상품 선택 로직
            if product_type == 'deposit':
                if risk <= 2:  # 안정 선호
                    weights = [0.95 if p.join_deny == 1 else 0.05 for p in products]
                else:  # 위험 선호
                    weights = [0.95 if hasattr(p, 'depositoptions') and 
                             p.depositoptions.filter(intr_rate__gt=3).exists() 
                             else 0.05 for p in products]
            
            elif product_type == 'saving':
                if risk <= 2:  # 안정 선호
                    weights = [0.95 if p.join_deny == 1 else 0.05 for p in products]
                else:  # 위험 선호
                    weights = [0.95 if hasattr(p, 'savingoptions') and 
                             p.savingoptions.filter(intr_rate__gt=4).exists() 
                             else 0.05 for p in products]
            
            else:  # mortgage
                if assets >= 5:  # 자산이 많은 경우
                    weights = [0.95 if hasattr(p, 'mortgageopions') and 
                             p.mortgageotions.filter(lend_rate_min__lt=4).exists() 
                             else 0.05 for p in products]
                else:
                    weights = [1/len(products)] * len(products)
            
            # 가중치 정규화
            weights = np.array(weights) / sum(weights)
            
            # 가중치 기반 무작위 선택
            y.append(np.random.choice(product_ids, p=weights))
            
        return X, np.array(y)

    def get_recommendations(self, user, n_recommendations=3):
        """사용자 기반 추천"""
        user_features = self._prepare_user_features(user)
        user_features_scaled = self.scaler.transform(user_features)
        
        recommendations = {}
        for product_type, model in self.models.items():
            if product_type == 'mortgage' and user.assets < 100000000:
                recommendations[product_type] = []
                continue
                
            # 각 상품에 대한 확률 예측
            probabilities = model.predict_proba(user_features_scaled)[0]
            top_n_indices = np.argsort(probabilities)[-n_recommendations:]
            
            # 상품 ID 가져오기
            product_ids = model.classes_[top_n_indices]
            
            # 상품 정보 조회
            if product_type == 'deposit':
                products = DepositProducts.objects.filter(id__in=product_ids)
            elif product_type == 'saving':
                products = SavingProducts.objects.filter(id__in=product_ids)
            else:
                products = MortgageProducts.objects.filter(id__in=product_ids)
                
            recommendations[product_type] = list(products)
            
        return recommendations