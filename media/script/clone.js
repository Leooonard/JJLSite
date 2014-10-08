(function(window, document){
     var clonehelper= function(){
          this.cloneillustration= function(src, prevFailCallback, prevSuccessCallback, nextFailCallback, nextSuccessCallback){
               var prevcopy= $(src).clone(true);
               var nextcopy= $(src).clone(true);
               var currentID= $(src).attr('data-id');
               // 先获取上一个对象.
               $.get('/ajaxprevillustration/'+ currentID+ '/', function(data){
                    if(data== 'failed'){
                         // 获取对象失败.
                         prevFailCallback();
                    }else{
                         // 获取对象成功.
                         obj= JSON.parse(data);
                         window.CURRENT_PAGE= parseInt(obj.page);
                         prevcopy.find('article.bigill_illustration img').attr('src', '/ueupload/'+ obj.path);
                         prevcopy.find('article.bigill_illtext p').text(obj.text);
                         prevcopy.attr('data-id', obj.id);
                         console.log('prev arrived!');
                         prevSuccessCallback(prevcopy);
                    }
               });
               // 获取下一个对象.
               $.get('/ajaxnextillustration/'+ currentID+ '/', function(data){
                    if(data== 'failed'){
                         // 获取对象失败.
                         nextFailCallback();
                    }else{
                         // 获取对象成功.
                         obj= JSON.parse(data);
                         window.CURRENT_PAGE= parseInt(obj.page);
                         nextcopy.find('article.bigill_illustration img').attr('src', '/ueupload/'+ obj.path);
                         nextcopy.find('article.bigill_illtext p').text(obj.text);
                         nextcopy.attr('data-id', obj.id);
                         console.log('next arrived!');
                         nextSuccessCallback(nextcopy);
                    }
               });
          }
          var that= this;
          this.prev= function(){
              var $this= $(this);
              // 解绑click事件, 防止多次点击, 当动画结束后, 重新进行绑定.
              $prevbtn.unbind('click');
              $nextbtn.unbind('click');
              $returnbtn.attr('disabled', '');
              window.PREVWRAPPER_ARRIVED= false;
              window.NEXTWRAPPER_ARRIVED= false;
              var callee= arguments.callee;
              // 处理滑动的函数!
              var prev= function(){
                  var $parent= $wrapper.parent();
                  $parent.css('overflow', 'hidden');
                  $nextwrapper= $wrapper.clone(true);
                  $parent.append($prevwrapper);
                  $prevwrapper.css('position', 'absolute');
                  $prevwrapper.css('top', '0px');
                  $prevwrapper.css('left', '-3000px');
                  $prevwrapper.animate({
                      left: '0px'
                  }, 1000);
                  $wrapper.animate({
                      left: '3000px'
                  }, 1100, function(){
                      /*$parent.empty();
                      $parent.append($prevwrapper);*/
                      $parent.css('overflow', 'visible');
                      $wrapper.remove();
                      $prevwrapper.css('position', 'relative');
                      // 获取新的上一个对象.
                      $wrapper= undefined;
                      $wrapper= $prevwrapper;
                      // $wrapper.find('#myshare_weixin').click(share);
                      // $wrapper.find('.myshare_qrcodeclose').click(close);
                      $prevwrapper= undefined;
                      $prevbtn.bind('click', that.prevloading);
                      $nextbtn.bind('click', that.nextloading);
                      $returnbtn.removeAttr('disabled');
                      $returnbtn.attr('data-url', '/illustration/?page='+ window.CURRENT_PAGE);
                      that.cloneillustration($wrapper, function(){
                          $prevbtn.css('display', 'none');
                          window.PREVWRAPPER_ARRIVED= true;
                          if(window.NEXTWRAPPER_ARRIVED== true&& window.PREVWRAPPER_ARRIVED){
                              $prevbtn.unbind('click');
                              $prevbtn.bind('click', that.prev);
                              $nextbtn.unbind('click');
                              $nextbtn.bind('click', that.next);
                          }
                      }, function(copy){
                          $prevwrapper= copy;
                          window.PREVWRAPPER_ARRIVED= true;
                          if(window.NEXTWRAPPER_ARRIVED== true&& window.PREVWRAPPER_ARRIVED){
                              $prevbtn.unbind('click');
                              $prevbtn.bind('click', that.prev);
                              $nextbtn.unbind('click');
                              $nextbtn.bind('click', that.next);
                          }
                      }, function(){
                          ;
                      }, function(copy){
                          $nextbtn.css('display', 'block');
                          window.NEXTWRAPPER_ARRIVED= true;
                          if(window.NEXTWRAPPER_ARRIVED== true&& window.PREVWRAPPER_ARRIVED){
                              $prevbtn.unbind('click');
                              $prevbtn.bind('click', that.prev);
                              $nextbtn.unbind('click');
                              $nextbtn.bind('click', that.next);
                          }
                      });    
                  });
              }            

              // 查看上一个容器是否读取完毕.
              if($prevwrapper== undefined&& $prevbtn.css('display')!= 'none'){
                  // 未读取完毕, 每隔0.5S读取一次.
                  setTimeout(function(){
                      if($prevwrapper== undefined&& $prevbtn.css('display')!= 'none'){
                          console.log('loading...');
                          setTimeout(arguments.callee, 500);
                      }else{
                        // 读取完毕或者不存在上一个.
                        if($prevwrapper!= undefined){
                            // 读取完毕. 删除现有容器, 然后添加新容器.
                            prev();
                        }else{
                          $prevbtn.bind('click', function(){
                              that.prev();
                          });
                          $nextbtn.bind('click', function(){
                              that.next();
                          });
                        }
                      }
                  }, 500);
              }else{
                  if($prevwrapper!= undefined){               
                      prev();
                  }else{
                     $prevbtn.bind('click', function(){
                         that.prev();
                     });
                     $nextbtn.bind('click', function(){
                         that.next();
                     });
                  }
              }
          };
          this.prevloading= function(){
              console.log('loading');
          };

          this.next= function(){
               var $this= $(this);
              // 解绑click事件, 防止多次点击, 当动画结束后, 重新进行绑定.
              $nextbtn.unbind('click');
              $prevbtn.unbind('click');
              $returnbtn.attr('disabled', '');
              window.PREVWRAPPER_ARRIVED= false;
              window.NEXTWRAPPER_ARRIVED= false;
              var callee= arguments.callee;
              // 滑动函数    
              var next= function(){    
                  var $parent= $wrapper.parent();
                  $parent.css('overflow', 'hidden');   
                  $prevwrapper= $wrapper.clone(true);
                  $parent.append($nextwrapper);
                  $nextwrapper.css('position', 'absolute');
                  $nextwrapper.css('top', '0px');
                  $nextwrapper.css('left', '3000px');
                  $nextwrapper.animate({
                      left: '0px'
                  }, 1000);
                  $wrapper.animate({
                      left: '-3000px'
                  }, 1100, function(){          
                      // 这里清空再加上去， 注册的事件为什么没有了？
                      // $parent.empty();
                      // $parent.append($nextwrapper);
                      $parent.css('overflow', 'visible');
                      $wrapper.remove();                       
                      $nextwrapper.css('position', 'relative');
                      // 获取新的上一个对象.
                      $wrapper= undefined;
                      $wrapper= $nextwrapper;
                      $nextwrapper= undefined;
                      $nextbtn.bind('click', that.nextloading);
                      $prevbtn.bind('click', that.prevloading);
                      $returnbtn.removeAttr('disabled');
                      $returnbtn.attr('data-url', '/illustration/?page='+ window.CURRENT_PAGE);
                      that.cloneillustration($wrapper, function(){
                          ;
                      }, function(copy){
                          // 防止到最后， 图标消失不会再出来.
                          $prevbtn.css('display', 'block');
                          window.PREVWRAPPER_ARRIVED= true;
                          if(window.NEXTWRAPPER_ARRIVED== true&& window.PREVWRAPPER_ARRIVED){
                              $prevbtn.unbind('click');
                              $prevbtn.bind('click', that.prev);
                              $nextbtn.unbind('click');
                              $nextbtn.bind('click', that.next);
                          }
                      }, function(){
                          $nextbtn.css('display', 'none');
                          window.NEXTWRAPPER_ARRIVED= true;
                          if(window.NEXTWRAPPER_ARRIVED== true&& window.PREVWRAPPER_ARRIVED){
                              $prevbtn.unbind('click');
                              $prevbtn.bind('click', that.prev);
                              $nextbtn.unbind('click');
                              $nextbtn.bind('click', that.next);
                          }
                      }, function(copy){
                          $nextwrapper= copy;
                          window.NEXTWRAPPER_ARRIVED= true;
                          if(window.NEXTWRAPPER_ARRIVED== true&& window.PREVWRAPPER_ARRIVED){
                              $prevbtn.unbind('click');
                              $prevbtn.bind('click', that.prev);
                              $nextbtn.unbind('click');
                              $nextbtn.bind('click', that.next);
                          }
                      });    
                  });
              }

              // 查看下一个容器是否读取完毕.
              if($nextwrapper== undefined&& $nextbtn.css('display')!= 'none'){
                  // 未读取完毕, 每隔0.5S读取一次.
                  setTimeout(function(){
                      if($nextwrapper== undefined== false&& $nextbtn.css('display')!= 'none'){
                          console.log('loading...');
                          setTimeout(arguments.callee, 500);
                      }else{
                        // 读取完毕或者不存在上一个.
                        if($nextwrapper!= undefined){
                            // 读取完毕. 删除现有容器, 然后添加新容器.
                            next();
                        }else{
                            $nextbtn.bind('click', function(){
                                   that.next();
                            });
                            $prevbtn.bind('click', function(){
                                   that.prev();
                            });
                        }
                      }
                  }, 500);
              }else{
                  if($nextwrapper!= undefined){                 
                      next();
                  }else{
                       $nextbtn.bind('click', function(){
                              that.next();
                       });
                       $prevbtn.bind('click', function(){
                              that.prev();
                       });
                  }
              }
          };
          this.nextloading= function(){
              console.log('loading');
          };
     };

     window['clonehelper']= clonehelper;
})(window, document)