        var i=0,j=0;
        var arr=['我就是我','每天一个反爬虫','我最帅','你不服?'];
        var arr1=['不一样的烟火','轻轻松松做前端','不接受反驳','不服也不行'];
        var but=['来 戳我','又来。。','畜生啊','够了吧','你牛逼'];
        var but1=[];
function init() {
            $('.left_text').animate({
                fontSize: '40px',
            }, 2000).animate({
                fontSize: '22px',
            }, 2000, function () {
                $('.right_text').animate({
                    fontSize: '40px',
                    marginLeft: '100px',
                }, 2000).animate({
                    fontSize: '22px',
                    marginLeft: '200px',
                }, 2000)
            })

        }

        function Size() {
            $('.login_content').click(function () {
                if (i == 4) {
                    i = 0;
                }
                $('.left_text').text(arr[i]);
                $('.right_text').text(arr1[i]);
                i++;
                init();
            })
        }

        function butConten() {

            $('.Me_image').hover(function () {
                $(this).removeClass('Me_image')
            },function () {
                $(this).addClass('Me_image')
            });



            $('.weixin_but').hover(function () {
                if(j==5){
                    j=0;
                }
                $(this).addClass("but1").text(but[j]).animate({
                    paddingLeft:'30px',
                });
                j= j+1;
            }, function () {
                $(this).removeClass("but1").text('微信轰炸').animate({
                    paddingLeft:'20px',
                });
            });




            $('.move_but').hover(function () {
                if(j==5){
                    j=0;
                }
                $(this).addClass('but1').text(but[j]).animate({
                    paddingLeft:'30px',
                });
                j++;
            },function () {
                $(this).removeClass("but1").text('新新电影').animate({
                    paddingLeft:'20px',
                })
            })
        }

        var c=0;
        function checkMain() {

           for (var m=0;m<12;m++) {
            $('.chat_text ul').append('<li></li>')
        }
            $('.buton').click(function () {
                $.ajax({
                    url:'/liaotian',
                    type:'GET',
                    data:{'date':$('.Mptext').val()},
                    dataType:'JSON',
                    success:function (arg) {
                        // if(c==12){
                        //     c=0;
                        // }
                        // $('.chat_text ul li').eq(11).text(arg);
                    }
                });
                c++;
            })
        }

        function xianshi() {
            $.ajax({
                url:'/xianshi',
                type:'GET',
                dataType:'JSON',
                success:function (arg) {
                    // console.log(arg);
                    if(arg.length==12){
                        $('.chat_text ul li').text('');
                    }
                    if(arg!=1) {
                        c=0;
                        for (var m = 0; m < arg.length; m++) {
                            if (c == 12) {
                                c = 0;
                            }
                            $('.chat_text ul li').eq(c).text(arg[m]);
                            c++;
                        }
                        xianshi()
                    }
                  xianshi()
                }
            })
        }


