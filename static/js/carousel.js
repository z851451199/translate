//轮播
function getByClass(oParent,sClass){
var aResult = [];
var aEle = oParent.getElementsByTagName('*');
	for(var i=0;i<aEle.length;i++){
		if(aEle[i].className==sClass){
			aResult.push(aEle[i]);
		}
	}
	return aResult;
}
	window.onload = function (){
		var oDiv = document.getElementById('playimages');
	var oBtnPrev = getByClass(oDiv,'prev')[0];
	var oBtnNext = getByClass(oDiv,'next')[0];
	var oMarkLeft = getByClass(oDiv,'mark_left')[0];
	var oMarkRight = getByClass(oDiv,'mark_right')[0];
	var oDivSmall = getByClass(oDiv,'small_pic')[0];
	var oUlSmall = oDivSmall.getElementsByTagName('ul')[0];
	var aLiSmall = oDivSmall.getElementsByTagName('li');
	var oUlBig = getByClass(oDiv,'big_pic')[0];
	var aLiBig = oUlBig.getElementsByTagName('li');
	var nowZIndex = 2;
	var now = 0;

	oUlSmall.style.width = aLiSmall[0].offsetWidth*aLiSmall.length+'px';
	//左右按钮
	oBtnPrev.onmouseover = oMarkLeft.onmouseover = function (){
		startMove(oBtnPrev,'opacity',100);
	}
	oBtnPrev.onmouseout = oMarkLeft.onmouseout = function (){
		startMove(oBtnPrev,'opacity',0);
	}
	oBtnNext.onmouseover = oMarkRight.onmouseover = function (){
		startMove(oBtnNext,'opacity',100);
	}
	oBtnNext.onmouseout = oMarkRight.onmouseout = function (){
		startMove(oBtnNext,'opacity',0);
	}
	//给小图的li加上事件
	for(var i=0;i<aLiSmall.length;i++){
		aLiSmall[i].index = i;
		aLiSmall[i].onclick = function (){
			if(this.index==now)return;
			now=this.index;
			tab();
		}
		aLiSmall[i].onmouseover = function (){
			startMove(this,'opacity',100);
		}
		aLiSmall[i].onmouseout = function (){
			if(this.index!=now){
				startMove(this,'opacity',60);
			}
			
		}
	}
      function tab(){
      	aLiBig[now].style.zIndex = nowZIndex++;
			for(var i=0;i<aLiSmall.length;i++){
				startMove(aLiSmall[i],'opacity',60);
			}
			startMove(aLiSmall[now],'opacity',100);
			aLiBig[now].style.height = 0;
			startMove(aLiBig[now],'height',900);
			if(now==0){
				startMove(oUlSmall,'top',0);
			}else if(now==aLiSmall.length-1){
				startMove(oUlSmall,'top',-(now-4)*aLiSmall[0].offsetHeight);
			}
      }
     //首先给左右按钮加上事件
     oBtnPrev.onclick = function (){
     	now--;
     	if(now==-1){
     		now = aLiSmall.length-1;
     	}
     	tab();
     }
     oBtnNext.onclick = function (){
     	now++;
     	if(now==aLiSmall.length){
     		now = 0;
     	}
     	tab();
     } 
     //鼠标移入图片时关闭定时器，首先定义一个变量接收定时器
     var  timer = setInterval( oBtnNext.onclick,3000);
     //然后给整个div加上事件，也就是移入到整个div时关闭定时器
     oDiv.onmouseover = function (){
     	clearInterval(timer);
     }
     //当鼠标移出时在把定时器打开
     oDiv.onmouseout = function (){
     	timer = setInterval( oBtnNext.onclick,3000);
     }
}
//各行变色
var oUl3 = document.getElementById("ul3");
var oLi = oUl3.getElementsByTagName('li');
for (var i=0;i<oLi.length;i++) {
	if(i%2==0){
		oLi[i].className = "active";
	}
}