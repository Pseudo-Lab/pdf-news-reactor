/**
 1. 기자 url parsing
 2. [api]api 호출로 url가 등록된 데이터인지 검증
 {
    "journalisturl" : "http://@"
 }
 2-1. 등록되지 않은 기자면 > 3번 > 4번
 2-2. 등록된 기자면 > 3번 스킵 > 사번
 3. (선택) url를 데이터에 삽입
 4. 기사의 기자 평가 parsing
 5. 평가가 모두 0이 아니면 > 7번 > 8번
 6. 평가가 모두 0이면 > 7번 스킵 > 8번
 7. [api](선택) uri로 평가 추가
  {
     "journalisturl" : "http://@",
     "useful" : @,
     "touched" : @,
     "recommend" : @,
     "analytical" : @,
     "wow" : @
  }
 8. [api]uri로 평가 평균 조회
   {
      "journalisturl" : "http://@",
   }
 9. 조회된 평균이 모두 0이면 > 12번
 10. 조회된 평균이 모두 0이 아니면 > 11번
 11. (결과 1) 평균을 chrome storage로 set
 12. (결과 2) "부족한 데이터로 조회가 어렵습니다." 표시
**/

let urlValue = "testurl";
let usefulcount = 9999;
let wowcount = 9999;
let touchedcount = 9999;
let analyticalcount = 9999;
let recommendcount = 9999;

const journalistNameElement = document.querySelector('.media_end_head_journalist_name');
//const journalistUrlElement = document.querySelector('div.media_journalistcard_summary_text a:first-child');
const journalistUrlElement = document.querySelector('a.media_journalistcard_summary_photo');
urlValue = journalistUrlElement.getAttribute('href');
console.log(urlValue);

if (journalistNameElement) {
  const journalistName = journalistNameElement.innerText.trim();
  chrome.storage.local.set({ journalist: journalistName }, function() {
    console.log("Journalist name saved:", journalistName);
  });
}

function update() {
  let likeCountElement = document.querySelectorAll('div._reactionModule.u_likeit.nv_notrans span.u_likeit_list_count._count');
  let usefulcount = parseInt(likeCountElement[0].textContent) || 0;
  let wowcount = parseInt(likeCountElement[1].textContent) || 0;
  let touchedcount = parseInt(likeCountElement[2].textContent) || 0;
  let analyticalcount = parseInt(likeCountElement[3].textContent) || 0;
  let recommendcount = parseInt(likeCountElement[4].textContent) || 0;

  console.log("journalisturl: ", urlValue)
  console.log("useful: ", usefulcount)
  console.log("wow: ", wowcount)
  console.log("touched: ", touchedcount)
  console.log("analytical: ", analyticalcount)
  console.log("recommend: ", recommendcount)

  chrome.storage.local.set(
                  {
                      journalisturl: urlValue,
                      useful: usefulcount,
                      wow: wowcount,
                      touched: touchedcount,
                      analytical: analyticalcount,
                      recommend: recommendcount,
                  },
                  function () {
                      console.log("Data stored in local storage");
                  }
              );
}

function validate() {
  try {
    const response = fetch("https://pdf.pseudolab-devfactory.com/api/journalist/validate", {
      method: "POST",
      body: JSON.stringify({
        "journalisturl": urlValue,
      }),
    });

    console.log(urlValue)
    console.log(response)

    if (!response.ok) {
      console.error("HTTP Error:", response.status);
      return false;
    }

    const result = response.json();

    if (typeof result === 'boolean') {
        console.log("Validation Result (boolean):", result);
        return result;
    }

    if (typeof result === 'object' && result !== null && 'isValid' in result) {
      console.log("Validation Result (object):", result.isValid);
      return result.isValid;
    }

    if (typeof result === 'object' && result !== null && 'result' in result) {
      console.log("Validation Result (object):", result.result);
      return result.result;
    }

    console.warn("Unexpected API response format:", result);
    return false;
  } catch (error) {
    console.error("Fetch Error:", error);
    return false;
  }
}


function add(usefulcount, wowcount, touchedcount, analyticalcount, recommendcount){
    try {
        const response = fetch("https://pdf.pseudolab-devfactory.com/api/journalist/add-score", {
          method: "POST",
          body: JSON.stringify({
            "journalisturl": urlValue,
            "useful": usefulcount,
            "touched": touchedcount,
            "recommend": recommendcount,
            "analytical": analyticalcount,
            "wow": wowcount
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = response.json();
        console.log("API Response:", result);
      } catch (error) {
        console.error("API Error:", error);
      };
}

function updateLikeCount() {
  const likeCountElement = document.querySelectorAll('div._reactionModule.u_likeit.nv_notrans span.u_likeit_list_count._count');
  const usefulcount = parseInt(likeCountElement[0].textContent) || 0;
  const wowcount = parseInt(likeCountElement[1].textContent) || 0;
  const touchedcount = parseInt(likeCountElement[2].textContent) || 0;
  const analyticalcount = parseInt(likeCountElement[3].textContent) || 0;
  const recommendcount = parseInt(likeCountElement[4].textContent) || 0;

  if (usefulcount === 0 && wowcount === 0 && touchedcount === 0 && analyticalcount === 0 && recommendcount === 0) {
    console.error("All like counts are zero. This is not allowed.");
    alert("모든 좋아요 수가 0입니다. 다시 시도해주세요.");
    return;
  }

  add(usefulcount, wowcount, touchedcount, analyticalcount, recommendcount);
}

function select() {
    try {
        const response = fetch("https://pdf.pseudolab-devfactory.com/api/journalist/average-score", {
            method: "POST",
            body: JSON.stringify({
                "journalisturl": urlValue,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = response.json();
        const allZero = Object.values(result).slice(1).every(value => value === 0);

        if (allZero) {
            console.log("부족한 데이터로 조회가 어렵습니다.");
            alert("부족한 데이터로 조회가 어렵습니다.");
        } else {
            chrome.storage.local.set(
                {
                    journalisturl: urlValue,
                    useful: usefulcount,
                    wow: wowcount,
                    touched: touchedcount,
                    analytical: analyticalcount,
                    recommend: recommendcount,
                },
                function () {
                    console.log("Data stored in local storage");
                }
            );
            console.log("Data stored:", result);
        }

    } catch (error) {
        console.error("Error fetching data:", error);
        alert("데이터 조회 중 오류가 발생했습니다.");
    }
}

fetch("https://pdf.pseudolab-devfactory.com/api/journalist/validate", {
  method: "POST",
  headers: {
    "Content-Type": "application/json", // Content-Type 헤더를 올바르게 설정합니다.
  },
  body: JSON.stringify({
    "journalisturl": "https://media.naver.com/journalist/001/78042",
  }),
})
  .then((response) => {
    console.log(response);
    if (response.status === 422) {
      // 422 오류 처리
      response.json().then((errorData) => {
        console.error("422 오류:", errorData);
      });
    }
  })
  .catch((error) => {
    console.error("Fetch 오류:", error);
  });

//setTimeout(function () {
//    update();
//    validate().then(isValid => {
//        if (isValid) {
//            console.log("Validation successful. Proceeding with updateLikeCount and then select.");
//            updateLikeCount();
//            select();
//        } else {
//            console.log("Validation failed. Proceeding directly to select.");
//            select();
//        }
//    });
//}, 1000);
