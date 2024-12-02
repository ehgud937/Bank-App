# chat/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from openai import OpenAI
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_message(request):
    conversation_id = request.data.get('conversation_id')
    if conversation_id:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    else:
        conversation = Conversation.objects.create(user=request.user)

    user_message = request.data.get('message')
    if not user_message:
        return Response({'error': '메시지를 입력해주세요.'}, 
                    status=status.HTTP_400_BAD_REQUEST)

    # 사용자 메시지 저장
    Message.objects.create(
        conversation=conversation,
        role='user',
        content=user_message
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 금융 상품 추천과 금융 관련 상담을 해주는 전문가입니다."},
                {"role": "user", "content": user_message}
            ]
        )
        
        ai_message = response.choices[0].message.content
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=ai_message
        )

        return Response({
            'conversation_id': conversation.id,
            'message': ai_message
        })

    except Exception as e:
        return Response({'error': str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_history(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data)