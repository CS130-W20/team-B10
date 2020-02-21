Survey
    .StylesManager
    .applyTheme("modern");

var json = {
    title: "Personalization Survey",
    showProgressBar: "bottom",
    firstPageIsStarted: true,
    startSurveyText: "Start Survey",
    pages: [
        {
            questions: [
                {
                    type: "html",
                    html: "You are about to answer some questions for us to better understand your preferences.<br/>Please click on <b>'Start Survey'</b> button when you are ready."
                }
            ]
        }, {
            questions: [
                {
                    type: "radiogroup",
                    name: "startday",
                    title: "When would you like to start your day during the trip?",
                    choices: [
                        "7:00 am", "8:00 am", "9:00 am", "10:00 am", "11:00 am"
                    ],
                }
            ]
        }, {
            questions: [
                {
                    type: "radiogroup",
                    name: "endday",
                    title: "When would you like to end your day during the trip?",
                    choices: [
                        "5:00 pm", "6:00 pm", "7:00 pm", "8:00 pm", "9:00 pm"
                    ],
                }
            ]
        }, {
            questions: [
                {
                    type: "radiogroup",
                    name: "numberofattractions",
                    title: "How many attractions would you like to visit everyday?",
                    choices: [
                        "1", "2", "3", "4"
                    ],
                }
            ]
        }
    ],
};

window.survey = new Survey.Model(json);

survey
    .onComplete
    .add(function (result) {
        document
            .querySelector('#surveyResult')
            .textContent = "Result JSON:\n" + JSON.stringify(result.data, null, 3);
    });

$("#surveyElement").Survey({model: survey});
