<script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=990c65316ad7b43897d80882ebd58ac1&libraries=services"></script>


<script>
const nextButton = document.getElementById('nextButton');
nextButton.addEventListener('click', function() {
window.location.href = "https://alice-qhkpb.run.goorm.site/service/temp/"; // 이동하려는 페이지의 URL
});
    
// 마커를 담을 배열입니다
var markers = [];
localStorage.clear();
var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 지도의 중심좌표
        level: 4 // 지도의 확대 레벨
    };  

// 지도를 생성합니다    
var map = new kakao.maps.Map(mapContainer, mapOption);

// 장소 검색 객체를 생성합니다
var ps = new kakao.maps.services.Places();  

// 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
var infowindow = new kakao.maps.InfoWindow({zIndex:1});
    


// 키워드로 장소를 검색합니다
searchPlaces();

// 키워드 검색을 요청하는 함수입니다
function searchPlaces(keyword) {
    

    // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
    ps.keywordSearch( keyword, placesSearchCB); 
}

// 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {

        // 정상적으로 검색이 완료됐으면
        // 검색 목록과 마커를 표출합니다
        displayPlaces(data);

        // 페이지 번호를 표출합니다
        displayPagination(pagination);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

        alert('검색 결과가 존재하지 않습니다.');
        return;

    } else if (status === kakao.maps.services.Status.ERROR) {

        alert('검색 결과 중 오류가 발생했습니다.');
        return;

    }
}

// 검색 결과 목록과 마커를 표출하는 함수입니다
function displayPlaces(places) {
   
    var listEl = document.getElementById('placesList'), 
    menuEl = document.getElementById('menu_wrap'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds(), 
    listStr = '';
    
    // 검색 결과 목록에 추가된 항목들을 제거합니다
    removeAllChildNods(listEl);
    var list = []

    // 지도에 표시되고 있는 마커를 제거합니다
    removeMarker();
    
    for ( var i=0; i<places.length; i++ ) {


        // 마커를 생성하고 지도에 표시합니다
        var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다
        console.log(places)
        
        var infor = {
            "place_name" : places[0].place_name,
            "road_address_name" : places[0].road_address_name,
            "address_name": places[0].address_name
        }
        localStorage.setItem("infor",JSON.stringify(infor));



        // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
        // LatLngBounds 객체에 좌표를 추가합니다
        bounds.extend(placePosition);


        // 마커와 검색결과 항목에 mouseover 했을때
        // 해당 장소에 인포윈도우에 장소명을 표시합니다
        // mouseout 했을 때는 인포윈도우를 닫습니다
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });

            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });

            itemEl.onmouseover =  function () {
                displayInfowindow(marker, title);
            };

            itemEl.onmouseout =  function () {
                infowindow.close();
            };
        })(marker, places[i].place_name);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
    listEl.appendChild(fragment);
    menuEl.scrollTop = 0;
  
    // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
    map.setBounds(bounds);
    if (places.length > 0) {
        displayRoadview(new kakao.maps.LatLng(places[0].y, places[0].x));
    }
}
    
var roadviewContainer = document.getElementById('roadview');
var roadview = new kakao.maps.Roadview(roadviewContainer);
var roadviewClient = new kakao.maps.RoadviewClient();
    


// 검색결과 항목을 Element로 반환하는 함수입니다
function getListItem(index, places) {

    var el = document.createElement('li'),
    itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                '<div class="info">' +
                '   <h5>' + places.place_name + '</h5>';

    if (places.road_address_name) {
        itemStr += '    <span>' + places.road_address_name + '</span>' +
                    '   <span class="jibun gray">' +  places.address_name  + '</span>';
    } else {
        itemStr += '    <span>' +  places.address_name  + '</span>'; 
    }
                 
      itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                '</div>';

    el.innerHTML = itemStr;
    el.className = 'item';


    return el;
}

// 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
function addMarker(position, idx, title) {
    var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png',
        imageSize = new kakao.maps.Size(36, 37),
        imgOptions = {
            spriteSize : new kakao.maps.Size(36, 691),
            spriteOrigin : new kakao.maps.Point(0, (idx*46)+10),
            offset: new kakao.maps.Point(13, 37)
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
        marker = new kakao.maps.Marker({
            position: position,
            image: markerImage
        });

    marker.setMap(map);

    // 마커를 클릭했을 때 로드뷰를 띄우는 함수

    // 마커 클릭 이벤트
    kakao.maps.event.addListener(marker, 'click', function() {
        displayRoadview(marker.getPosition());
    });

    // 첫 번째 마커에 대해서만 자동으로 로드뷰를 띄움

    return marker;
}
function displayRoadview(latlng) {
        roadviewClient.getNearestPanoId(latlng, 50, function(panoId) {
            roadview.setPanoId(panoId, latlng);
        });
    }



// 지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function displayPagination(pagination) {
    var paginationEl = document.getElementById('pagination'),
        fragment = document.createDocumentFragment(),
        i; 

    // 기존에 추가된 페이지번호를 삭제합니다
    while (paginationEl.hasChildNodes()) {
        paginationEl.removeChild (paginationEl.lastChild);
    }

    for (i=1; i<=pagination.last; i++) {
        var el = document.createElement('a');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.className = 'on';
        } else {
            el.onclick = (function(i) {
                return function() {
                    pagination.gotoPage(i);
                }
            })(i);
        }

        fragment.appendChild(el);
    }
    paginationEl.appendChild(fragment);
}

// 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
// 인포윈도우에 장소명을 표시합니다
function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

 // 검색결과 목록의 자식 Element를 제거하는 함수입니다
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}
        let mediaRecorder;
        let recordedChunks = [];
        function convertAudioToText() {
            var audioFile = document.getElementById('audioFile').files[0];
            if (!audioFile) {
                alert('Please select an audio file.');
                return;
            }

            var formData = new FormData();
            formData.append('audio', audioFile);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '{% url "convert_audio" %}', true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        var response = JSON.parse(xhr.responseText);
                        displayConvertedText(response.text);
                        displayConvertedProb(response.code.prob);
                        displayConvertedCode(response.code.count);
                        displayConvertedGet(response.code.get);
                        displayConvertedImage();

                        var textinfor = {
                            "code" : response.code,
                            "text" : response.text
                             }
                        localStorage.setItem("textinfor",JSON.stringify(textinfor));

                        searchPlaces(response.words_with_label_25);
                    } else {
                        alert('Server error occurred.');
                    }
                }
            };
            xhr.send(formData);
        }


        const startRecording = async () => {
            recordedChunks = [];
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', blob);

                const xhr = new XMLHttpRequest();
                xhr.open('POST', '{% url "convert_audio" %}', true);
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === XMLHttpRequest.DONE) {
                        if (xhr.status === 200) {
                            const response = JSON.parse(xhr.responseText);
                            displayConvertedText(response.text);
                            displayConvertedProb(response.code.prob);
                            displayConvertedCode(response.code.count);
                            displayConvertedGet(response.code.get);
                            displayConvertedImage();
                            var textinfor = {
                                "code" : response.code,
                                "text" : response.text
                                 }
                            localStorage.setItem("textinfor",JSON.stringify(textinfor));

                            searchPlaces(response.words_with_label_25);
                            
                        
                        } else {
                            alert('Server error occurred.');
                        }
                    }
                };
                xhr.send(formData);
            };

            mediaRecorder.start();
            document.getElementById('startRecordButton').disabled = true;
            document.getElementById('stopRecordButton').disabled = false;
            document.getElementById('convertButton').disabled = true;
        };

        const stopRecording = () => {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                document.getElementById('startRecordButton').disabled = false;
                document.getElementById('stopRecordButton').disabled = true;
                document.getElementById('convertButton').disabled = false;
            }
        };

        function displayConvertedText(text) {
            var convertedTextDiv = document.getElementById('convertedText');
            convertedTextDiv.innerHTML = text;
        }
        function displayConvertedImage() {
            var additionalPhotosElement = document.getElementById('convertedImage');
                
            
additionalPhotosElement.innerHTML = '<img src="{% static "safety_zisoo.png" %}" alt="Safety Zisoo Image" class="safety">' + '<img src="{% static "graph_output_2.png" %}?t=' + new Date().getTime() + '" alt="추가 사진 1">';


        function displayConvertedCode(code) {
            var convertedTextDiv = document.getElementById('Code');
            convertedTextDiv.innerHTML = code;            
        }
        function displayConvertedProb(prob) {
            var convertedTextDiv = document.getElementById('prob');
            convertedTextDiv.innerHTML = prob;            
        }
        function displayConvertedGet(get) {
            var convertedTextDiv = document.getElementById('get');
            convertedTextDiv.innerHTML = get;            
        }
    
    

        document.getElementById('startRecordButton').addEventListener('click', startRecording);
        document.getElementById('stopRecordButton').addEventListener('click', stopRecording);
    let isRecording = false;
    setInterval(() => {
        if (isRecording) {

            document.getElementById('indicator').style.visibility = 'hidden';
            setTimeout(() => {

                if (!isRecording) {
                    document.getElementById('indicator').style.visibility = 'hidden';
                } else {
                    document.getElementById('indicator').style.visibility = 'visible';
                }
            }, 500);
        }
    }, 1000);

    document.getElementById('startRecordButton').addEventListener('click', () => {
        startRecording();
        isRecording = true;
    });

    document.getElementById('stopRecordButton').addEventListener('click', () => {
        stopRecording();
        isRecording = false;
        document.getElementById('indicator').style.visibility = 'hidden';
    });
    // 페이지 이동 버튼 클릭 이벤트 처리
    var linkToTempButton = document.getElementById("nextButton");
    linkToTempButton.addEventListener("click", function() {
        // index_final.html로 페이지 이동
        window.location.href = "https://alice-itfcs.run.goorm.site/service/temp/";
    });
function showDescription(photoId) {
  const titleElement = document.getElementById('photo-title');
  const descriptionElement = document.getElementById('photo-description');
  const additionalPhotosElement = document.getElementById('additional-photos');

  if (photoId === 'photo1') {
    additionalPhotosElement.innerHTML = '<img src="{% static "graph_output_1.png" %}?t=' + new Date().getTime() + '" alt="추가 사진 1">';
}
  const description = document.getElementById('description');
  description.style.display = 'block';

  // description 영역을 클릭하면 다시 숨기도록 설정
  description.addEventListener('click', function () {
    description.style.display = 'none';
  });
}
        } </script>