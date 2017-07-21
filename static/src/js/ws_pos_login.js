/**
 @项目: wensfood
 @模块名称
 @Copyright 2016 WENS <www.wens.com.cn>
 @Created by LiJiaJie at 2017/5/11 上午12:31
 **/



//登录方法
function action_login() {
    var login =$('#txt_login').val();
    var password =$('#txt_password').val();
    var code = '001'; // getCookie('distribution_dc_code');
    var wh_id = '93';// getCookie('distribution_wh_id');

     login = '13929842439';
     password = '11';
    var params = {
        'code': code,
        'login': login,
        'password': password
    }

    //删除cookie
    delCookie('distribution_user_id');
    delCookie('distribution_user_name');
    delCookie('distribution_user_sid');
    delCookie('distribution_wh_id');

    //判断用户名和密码是否为空
    if(login != "" && password != ""){
        //发送登录请求
        $.post('/distribution/user/login', params, function (data) {
            var result = JSON.parse(data);
            console.log(result);

            if(result['code'] == 0){
                var result_data = result['data'];
                var user_id = result_data['user_id'];
                var user_name = result_data['user_name'];
                var session_id = result_data['session_id'];

                setCookie('distribution_dc_code', code);
                setCookie('distribution_wh_id', wh_id);
                setCookie('distribution_user_id', user_id);
                setCookie('distribution_user_name', user_name);
                setCookie('distribution_user_sid', session_id);

                $('#id_distribution').click();
            }else{
                alert(result['msg']);
            }

        });
    }
    else if(login == ""){
        alert("请输入用户名！")
    }
    else if(password == ""){
        alert("请输入密码！")
    }

}

//=============================使用cookie的方法==============================================
//新增cookie
function setCookie(name,value)
{
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days*24*60*60*1000);
    document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}

//读取cookies
function getCookie(name)
{
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");

    if(arr=document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

//删除cookies
function delCookie(name)
{
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var val = getCookie(name);
    if(val != null)
        document.cookie = name + "=" + val+";expires=" + exp.toGMTString();
}