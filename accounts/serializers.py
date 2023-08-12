# accounts/serializers.py
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    
    class Meta:
        model = Member
        exclude = ['refresh_token']
        
    def save(self, request):

        member = Member.objects.create(
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            is_mentor=self.validated_data['is_mentor'],
            kor_univ=self.validated_data['kor_univ'],
            kor_major=self.validated_data['kor_major'],
            kor_email=self.validated_data['kor_email'],
            # continent=self.validated_data['continent'],
            # contry=self.validated_data['contry'],
            # language=self.validated_data['language'],
            # foreign_univ=self.validated_data['foreign_univ'],
            # foreign_major=self.validated_data['foreign_major'],
            # foreign_email=self.validated_data['foreign_email'],
            # exchangeSemester=self.validated_data['exchangeSemester'],
            # exchangeDuration=self.validated_data['exchangeDuration'],
        )
				
		# password 암호화
        member.set_password(self.validated_data['password'])
        member.save()

        return member
    
    def validate(self, data):
        username = data.get('username', None)
        name = data.get('name', None)
        kor_univ = data.get('kor_univ', None)
        kor_major = data.get('kor_major', None)
        kor_email = data.get('kor_email', None)
        is_mento = data.get('is_mento', None)
        continent = data.get('continent', None)
        contry = data.get('contry', None)
        language = data.get('language', None)
        foreign_univ = data.get('foreign_univ', None)
        foreign_major = data.get('foreign_major', None)
        foreign_email = data.get('foreign_email', None)
        exchangeSemester = data.get('exchangeSemester', None)
        exchangeDuration = data.get('exchangeDuration', None)
         

        if Member.objects.filter(name=name).exists():
            raise serializers.ValidationError('이미 존재하는 이름입니다.')
        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError('이미 존재하는 아이디입니다.')
        
        return data
    
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Member
        fields = ['username', 'password']
        
    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

	    # Member DB에서 요청의 username과 일치하는 데이터가 존재하는지 확인함
        if Member.objects.filter(username=username).exists():
            member = Member.objects.get(username=username)
	    
				# DB에 해당 데이터가 존재하는데 password가 일치하지 않는 경우
            if not member.check_password(password):
                raise serializers.ValidationError("잘못된 비밀번호 입니다.")
        else:
            raise serializers.ValidationError("존재하지 않는 회원입니다.")
	        
        token = RefreshToken.for_user(member)
        refresh_token = str(token)
        access_token = str(token.access_token)
	
        data = {
			    'member':member,
			    'refresh_token':refresh_token,
			    'access_token':access_token,
        }
        
        return data