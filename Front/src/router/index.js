import { createRouter, createWebHistory } from 'vue-router'

import Homeview from '@/views/Homeview.vue'

import BankMapView from '@/views/BankMapView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'
import LoginView from '@/views/LoginView.vue'
import KakaoCallbackView from '@/views/KakaoCallbackView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ModifyProfileView from '@/views/ModifyProfileView.vue'
import SignOutView from '@/views/SignOutView.vue'

import ProductListView from '@/views/ProductList/ProductListView.vue'
import DepositProductView from '@/views/ProductList/DepositProductView.vue'
import DepositProductDetailView from '@/views/ProductList/DepositProductDetailView.vue'
import SavingProductView from '@/views/ProductList/SavingProductView.vue'
import SavingProductDetailView from '@/views/ProductList/SavingProductDetailView.vue'
import MortgageProductView from '@/views/ProductList/MortgageProductView.vue'
import MortgageProductDetailView from '@/views/ProductList/MortgageProductDetailView.vue'

import CommunityView from '@/views/CommunityView.vue'
import CommunityListAll from '@/views/CommunityDetail/CommunityListAll.vue'
import CommunityListAsk from '@/views/CommunityDetail/CommunityListAsk.vue'
import CommunityListFree from '@/views/CommunityDetail/CommunityListFree.vue'
import CommunityListReview from '@/views/CommunityDetail/CommunityListReview.vue'
import ComminityListEtc from '@/views/CommunityDetail/ComminityListEtc.vue'
import CommunityDetailView from '@/views/CommunityDetail/CommunityDetailView.vue'
import CommunityListNotice from '@/views/CommunityDetail/CommunityListNotice.vue'
import CreateCommunityArticleView from '@/views/CommunityDetail/CreateCommunityArticleView.vue'
import ModifyCommunityArticleView from '@/views/CommunityDetail/ModifyCommunityArticleView.vue'
import ModifyCommunityCommentView from '@/views/CommunityDetail/ModifyCommunityCommentView.vue'

import RecommendView from '@/views/RecommendView.vue'
import RecommendForYouView from '@/views/Recommend/RecommendForYouView.vue'
import RecommendUserInfoView from '@/views/Recommend/RecommendUserInfoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Homeview,
    },
    {
      path: '/bankmap',
      name: 'bankmap',
      component: BankMapView,
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeRateView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/modify-profile',
      name: 'modify-profile',
      component: ModifyProfileView,
    },
    {
      path: '/signout',
      name: 'signout',
      component: SignOutView,
    },
    {
      path: '/product',
      name: 'product',
      component: ProductListView,
      children: [
        { path: 'deposit', name: 'deposit-product', component: DepositProductView },
        { path: 'deposit/:id', name: 'deposit-product-detail', component: DepositProductDetailView },
        { path: 'saving', name: 'saving-product', component: SavingProductView },
        { path: 'saving/:id', name: 'saving-product-detail', component: SavingProductDetailView },
        { path: 'mortgage', name: 'mortgage-product', component: MortgageProductView },
        { path: 'mortgage/:id', name: 'mortgage-product-detail', component: MortgageProductDetailView },
      ]
    },
    {
      path: '/exchange',
      name: 'exchange-rate',
      component: ExchangeRateView,
    },
    {
      path: '/bankmap',
      name: 'bankmap',
      component: BankMapView,
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView,
      children: [
        { path: 'all', name: 'community_all', component: CommunityListAll },
        { path: 'free', name: 'community_free', component: CommunityListFree },
        { path: 'ask', name: 'community_ask', component: CommunityListAsk },
        { path: 'review', name: 'community_review', component: CommunityListReview },
        { path: 'etc', name: 'community_etc', component: ComminityListEtc },
        { path: 'notice', name: 'community_notice', component: CommunityListNotice },
        { path: 'detail/:id', name: 'article-detail', component: CommunityDetailView },
        { path: 'create-article', name: 'create-article', component: CreateCommunityArticleView },
        { path: 'modify-article/:id', name: 'modify-article', component: ModifyCommunityArticleView },
        { path: 'article/:id/comment/:cid', name: 'modify-comment', component: ModifyCommunityCommentView },
      ]
    },
    {
      path: '/recommend',
      name: 'recommend',
      component: RecommendView,
      children: [
        { path: 'for-you', name: 'recommend_for_you', component: RecommendForYouView },
        { path: 'user-info', name: 'recommend_user_info', component: RecommendUserInfoView },
      ]
    },
    {
      path: '/accounts/kakao/callback',
      name: 'kakao-callback',
      component: KakaoCallbackView
    },
  ],
})

export default router
