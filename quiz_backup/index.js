const logStyle = `
  background-color: darkblue; 
  color: white; 
  font-style: 
  italic; padding:.2em; 
  font-size: 30px;
`;

document.addEventListener("DOMContentLoaded", () => {
  
  // ------------------------------------------------------
  // @SHARE-API  ------------------------------------------
  // ------------------------------------------------------

  let shareData = {
    title: "Sando Personality Quiz",
    text: "Which sando are you?",
    url: "https://counterservice.com/quiz",
  };

  const btn = document.querySelector("#share-api");
  const resultPara = document.querySelector("#share-result");

  // Share must be triggered by "user activation"
  btn.addEventListener("click", async () => {
    try {
      await navigator.share(shareData);
      // resultPara.style.color = "green";
      // resultPara.textContent = "shared successfully";
      console.log(`shared successfully`)
    } catch (err) {
      // resultPara.style.color = "red";
      // resultPara.textContent = `Error: ${err}`;
      console.log(`Error: ${err}`);
    }
  });

  // ------------------------------------------------------
  // @SHARE-BUTTON  ---------------------------------------
  // ------------------------------------------------------

  const shareButton = document.getElementById("share");
  // shareButton.textContent = "Share"
  // shareButton.id = "share"

  shareButton.onclick = () => {
    const shareMessage = `${shareData.title} - ${shareData.text}\rTry it out at ${shareData.url}`;
    navigator.clipboard
      .writeText(shareMessage)
      .then(() => {
        alert(`Copied to clipboard:\r\r${shareMessage}`);
      })
      .catch((err) => {
        alert("Failed to copy link. Please try again.");
      });
  };

  function drawQuiz(
    answerTextArray,
    choicesTextArray,
    pointsArray,
    profilesJSON
  ) {
    // ------------------------------------------------------
    // @DRAWQUIZ VARIABLES ---------------------------------
    // ------------------------------------------------------

    let answerText = choicesTextArray;
    let answerValues = [];
    const buttonElement = document.getElementById("button");
    const quiz = document.getElementById("quiz");
    let questionState = 0;
    let quizActive = true;
    let questionText = answerTextArray;
    const results = document.getElementById("results");
    let totalPoints = 0;

    // ------------------------------------------------------
    // * drawQuiz METHODS -----------------------------------
    // ------------------------------------------------------

    // - U P D A T E - Q U I Z - S T A T E ----------------
    
    function updateQuizState() {
      updateProfile();

      if (quizActive) {
        drawQuestion(questionState);
        questionState++;
        buttonElement.disabled = true;
        buttonElement.innerHTML = "Please select an answer";
        buttonElement.style.opacity = 0.7;
      } else {
        drawProfilePage();
      }
    }

    function drawQuestion(question) {
      
      let answerSelection = ``;
      
      for (i = 0; i < answerText[question].length; i++) {
        let answerChoice = answerText[question][i];
        let letter = String.fromCharCode(65 + i);
        answerSelection += `
          <li> 
            <input type="radio" name="question${question+1}" onClick="window.setAnswer(${i},${question})" id="${answerChoice}" />
                  <label for="${answerChoice}">
                  <div>${letter}.</b> </div>
                  <div>${answerChoice}</div>
                  </label>
          </li>`;
      }

      document.getElementById("questions").innerHTML = questionText[question];
      document.getElementById("answers").innerHTML = answerSelection;
    }

    function setAnswer(input, questionIndex) {
      answerValues[questionIndex] = pointsArray[questionIndex][input];
      let letter = String.fromCharCode(65 + input);
      console.log(
        `%c#${questionIndex + 1} | ${letter}  +${
          pointsArray[questionIndex][input]
        }`,
        logStyle
      );

      if (questionState < questionText.length) {
        buttonElement.innerHTML = "Continue";
        buttonElement.disabled = false;
        buttonElement.style.opacity = 1;
      } else {
        quizActive = false;
        buttonElement.innerHTML = "Crunch Numbers";
        buttonElement.disabled = false;
        buttonElement.style.opacity = 1;
      }
    }

    function updateProfile() {
      totalPoints = answerValues.reduce(
        (total, current) => total + Number(current),
        0
      );

      console.clear();
      console.log(`%cTotal Points: ${totalPoints}`, logStyle);
      document.title = `Quiz | ${answerValues.length}/${questionText.length} | Points: ${totalPoints}`;
    }

    function drawProfilePage() {
      quiz.style.display = "none";
      results.style.display = "block";
      let resultsInfo;
      profilesJSON.forEach((profile) => {
        let lowerBound = parseInt(profile["Lower Bound"]);
        let upperBound = parseInt(profile["Upper Bound"]);
        if (totalPoints >= lowerBound && totalPoints <= upperBound) {
          resultsInfo = profile;
        }
        // console.log(
        //   totalPoints,
        //   totalPoints >= lowerBound && totalPoints <= upperBound
        // );
      });

      shareData.text += `\r-\rI'm the ${resultsInfo["Sandwich"]} - ${resultsInfo["You Are:"]}`;

      results.innerHTML = `
     
        <!-- <h1>${totalPoints}</h1> -->
        <h2>${resultsInfo["You Are:"]}</h2>
        <h3>${resultsInfo["Sandwich"]}</h3>

        <p>${resultsInfo["Description"]}</p>
        <button class="button" onClick="window.location.href=window.location.href">
          Restart quiz
        </button>
        <!-- <pre>${JSON.stringify(resultsInfo, null, 2)}</pre> -->
    `;
      shareButton.setAttribute("data-result", resultsInfo["You Are:"]);
      // results.appendChild(shareButton)
    }

    buttonElement.addEventListener("click", updateQuizState);
    window.setAnswer = setAnswer;
  }

  // ------------------------------------------------------
  // @SHEETDB CONFIG --------------------------------------
  // ------------------------------------------------------

  let sheetDB = {
    enpoint: `https://sheetdb.io/api/v1/c1ckdgz5om2wt`,
  };

  sheetDB = {
    ...sheetDB,
    info: {
      live: `${sheetDB.enpoint}/name`,
      cached: "cached/cached.info.json",
    },
    quiz: {
      live: `${sheetDB.enpoint}?sheet=Quiz%20Questions%20and%20Feedback`,
      cached: "cached/cached.quiz.json",
    },
    scoring: {
      live: `${sheetDB.enpoint}?sheet=Scoring Matrix`,
      cached: `cached/cached.scoring.json`,
    },
    profiles: {
      live: `${sheetDB.enpoint}?sheet=Results Profiles`,
      cached: "cached/cached.profiles.json",
    },
  };

  fetchAll(sheetDB.quiz.cached, sheetDB.scoring.cached, sheetDB.profiles.cached)
    .then((results) => {
      let quizJSON = results.response1;
      let scoreJSON = results.response2;
      let profilesJSON = results.response3;
      let answerTextArray = [];
      let choicesTextArray = [];
      let pointsArray = [];

      Object.keys(quizJSON).forEach((json, i) => {
        answerTextArray.push(quizJSON[json]["Question"]);
        choicesTextArray.push([
          quizJSON[json]["A"],
          quizJSON[json]["B"],
          quizJSON[json]["C"],
          quizJSON[json]["D"],
        ]);
        pointsArray.push([
          scoreJSON[i]["A"],
          scoreJSON[i]["B"],
          scoreJSON[i]["C"],
          scoreJSON[i]["D"],
        ]);
      });

      drawQuiz(answerTextArray, choicesTextArray, pointsArray, profilesJSON);
    })
    .catch((error) => {
      console.error("Failed to fetch data:", error);
    });
});
