var vue = new Vue({
    el:'#inputBackground',
    data:{
        usernameInput: '',
        passwordInput: '',
    },
    methods:{
        login:function(){
            var parameters = JSON.stringify({'username':this.usernameInput,  'password':this.passwordInput})
            this.$http.post('/Login', {'command':'login','parameter':parameters}).then(function(res){
                if (res.body == 'SIGNAU_User_Does_Not_Exist'){
                    alert('用户名不存在')
                }
                else if (res.body == 'SIGNAU_Password_Wrong'){
                    alert('密码错误')
                }
                else if (res.body.length == 36){
                    alert('登录成功')
                    location.href='Welcome'
                }

            },function(){
                console.log('Error');
            });
        },
        signUp:function(){
            var parameters = JSON.stringify({'username':this.usernameInput,  'password':this.passwordInput})
            this.$http.post('/Login', {'command':'signUp','parameter':parameters}).then(function(res){
                console.log(res.body);  
                if (res.body == 'SIGNAU_SignUp_Success'){
                    alert('注册成功')
                }
                else if (res.body == 'SIGNAU_Username_or_Password_Illegel'){
                    alert('注册失败')
                }  
            },function(){
                console.log('Error');
            });
        },
    },
})