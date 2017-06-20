var motion_num = 0;
function motion_visual(){
	setTimeout(function(){
		$(".visual_img li").removeClass("on");
		$(".visual_img li").eq(0).addClass("on");
	},12000)

	motion1 = setInterval(function(){
		var max = $(".visual_img li").length;

		if (motion_num < max)
		{
			motion_num = motion_num+1;
		}else{
			motion_num = 1;
		}

		$(".visual_img li").removeClass("on");
		$(".visual_img li").eq(motion_num-1).addClass("on");
	},12000);

};


$(function(){
	motion_visual();
});