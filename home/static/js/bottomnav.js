//for tabs open
    function shopBottomnav(cityName,elmnt,color) {
      var i, tabcontent, tablinks;
      if(cityName=='apka_shop_additem_body')
      {
      $('#'+cityName).css("height",'395px');
      }else{
      $('#'+cityName).css("height",'440px');
      }

      tabcontent = document.getElementsByClassName("apka_shop_bottom_content");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("apka_shop_bottom_nav_data");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "";
      }
      document.getElementById(cityName).style.display = "block";
      elmnt.style.backgroundColor = color;
    
    }
// Get the element with id="defaultOpen" and click on it
    document.getElementById("defaultOpen").click();

