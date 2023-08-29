<script>
window.onload = function() {
    
    var castdata = JSON.parse(localStorage.getItem("infor"));
    var textdata = JSON.parse(localStorage.getItem("textinfor"));
    var locationInput = document.getElementById("location");
    var addressInput = document.getElementById("address");
    if (textdata.code.count == "CODE0"){
        var checkboxes= document.getElementById("code0Checkbox");
        checkboxes.checked=true;
    }
    if (textdata.code.count == "CODE1"){
        var checkboxes= document.getElementById("code1Checkbox");
        checkboxes.checked=true;
    }
    if (textdata.code.count == "CODE2"){
        var checkboxes= document.getElementById("code2Checkbox");
        checkboxes.checked=true;
    }
    if (textdata.code.count == "CODE3"){
        var checkboxes= document.getElementById("code3Checkbox");
        checkboxes.checked=true;
    }
    if (textdata.code.count == "CODE4"){
        var checkboxes= document.getElementById("code4Checkbox");
        checkboxes.checked=true;
    }

    var roadaddressInput = document.getElementById("jibunAddress");
    console.log(textdata)
    var reportContentInput = document.getElementById("reportContent");
    var probInput=document.getElementById("codeprob");
    
    locationInput.value = castdata.place_name;
    roadaddressInput.value = castdata.road_address_name;
    addressInput.value = castdata.address_name;
    reportContentInput.value=textdata.text;
    
}
</script>