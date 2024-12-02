# register/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import DepositRegister, SavingRegister, MortgageRegister, RegisterStatus
from .serializers import (
    DepositRegisterSerializer, 
    SavingRegisterSerializer, 
    MortgageRegisterSerializer
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import resend
	
resend.api_key = settings.RESEND_API_KEY
# def send_register_email(user_email, product_name, register_type):
#     """가입 신청 완료 메일 전송"""
#     subject = f'[금융상품] {product_name} 가입 신청이 완료되었습니다.'
    
#     # HTML 템플릿 렌더링
#     html_message = render_to_string('register/email/register_complete.html', {
#         'product_name': product_name,
#         'register_type': register_type
#     })
    
#     # 플레인 텍스트 버전 생성
#     plain_message = strip_tags(html_message)
    
#     # 메일 발송
#     send_mail(
#         subject=subject,
#         message=plain_message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[user_email],
#         html_message=html_message,
#         fail_silently=False,
#     )

def send_register_email(user_email, product_name, register_type):
    try:
        subject = f'[금융상품] {product_name} 가입 신청이 완료되었습니다.'
        message = f"""
안녕하세요.

{product_name} {register_type} 상품 가입 신청이 완료되었습니다.
신청하신 내용은 검토 후 승인 여부를 다시 안내드리겠습니다.

감사합니다.

※ 본 메일은 발신전용 메일입니다.
        """
        
        print(f"Attempting to send email to: {user_email}")  # 디버깅용
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        print("Email sent successfully")  # 디버깅용
        
    except Exception as e:
        print(f"Detailed email error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise

def send_register2_email(user_email, product_name, register_type):
    try:
        subject = f'[금융상품] {product_name} 가입 신청이 완료되었습니다.'
        
        # HTML 템플릿 직접 작성
        html_content = f'''
        <div style='font-family: Arial, sans-serif; line-height: 1.6;'>
            <p>안녕하세요.</p>
            <p>{product_name} {register_type} 상품 가입 신청이 완료되었습니다.</p>
            <p>신청하신 내용은 검토 후 승인 여부를 다시 안내드리겠습니다.</p>
            <p>감사합니다.</p>
            <p>※ 본 메일은 발신전용 메일입니다.</p>
        </div>
        '''
        
        print(f"Attempting to send email to: {user_email}")
        
        params = {
            "from": "onboarding@resend.dev",
            "to": user_email,
            "subject": subject,
            "html": html_content
        }
        
        email = resend.Emails.send(params)
        print("Email sent successfully with ID:", email['id'])
        return email['id']
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_deposit(request, product_id, option_id):
    serializer = DepositRegisterSerializer(data={
        'product': product_id,
        'option': option_id,
    })
    if serializer.is_valid():
        register = serializer.save(user=request.user)
        
        # 이메일 발송
        try:
            send_register_email(
                user_email=request.user.email,
                product_name=register.product.fin_prdt_nm,
                register_type='예금'
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

        try:
            send_register2_email(
                user_email='ehgud937@gmail.com',
                product_name=register.product.fin_prdt_nm,
                register_type='예금'
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_saving(request, product_id, option_id):
    serializer = SavingRegisterSerializer(data={
        'product': product_id,
        'option': option_id,
    })
    if serializer.is_valid():
        register = serializer.save(user=request.user)
        
        # 이메일 발송
        try:
            send_register_email(
                user_email=request.user.email,
                product_name=register.product.fin_prdt_nm,
                register_type='적금'
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

        try:
            send_register2_email(
                user_email='ehgud937@gmail.com',
                product_name=register.product.fin_prdt_nm,
                register_type='예금'
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_mortgage(request, product_id, option_id):
    serializer = MortgageRegisterSerializer(data={
        'product': product_id,
        'option': option_id,
    })
    if serializer.is_valid():
        register = serializer.save(user=request.user)
        
        # 이메일 발송
        try:
            send_register_email(
                user_email=request.user.email,
                product_name=register.product.fin_prdt_nm,
                register_type='주택담보대출'
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

        try:
            send_register2_email(
                user_email='ehgud937@gmail.com',
                product_name=register.product.fin_prdt_nm,
                register_type='예금'
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_registers(request):
    deposits = DepositRegister.objects.filter(user=request.user)
    savings = SavingRegister.objects.filter(user=request.user)
    mortgages = MortgageRegister.objects.filter(user=request.user)
    
    return Response({
        'deposits': DepositRegisterSerializer(deposits, many=True).data,
        'savings': SavingRegisterSerializer(savings, many=True).data,
        'mortgages': MortgageRegisterSerializer(mortgages, many=True).data
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_register(request, register_type, register_id):
    if register_type == 'deposit':
        register = get_object_or_404(DepositRegister, id=register_id, user=request.user)
    elif register_type == 'saving':
        register = get_object_or_404(SavingRegister, id=register_id, user=request.user)
    elif register_type == 'mortgage':
        register = get_object_or_404(MortgageRegister, id=register_id, user=request.user)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    register.status = RegisterStatus.CANCELLED
    register.save()
    return Response(status=status.HTTP_204_NO_CONTENT)