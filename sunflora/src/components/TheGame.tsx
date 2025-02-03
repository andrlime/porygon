import { useEffect, useState } from "react";
import "./Game.css"
import axios from "axios";

interface IPage {
    propagateState: (str: string) => void;
    maxQuestionCount: number;
}

interface Response {
    response_text: string;
    scores: Array<number>;
}

interface Question {
    question_text: string;
    responses: Array<Response>;
}

export const TheGame: React.FC<IPage> = ({ propagateState, maxQuestionCount }) => {
    const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
    const [questionCount, setQuestionCount] = useState(0);
    const [gameOver, setGameOver] = useState(false);

    const scoreLabels = ["harmony", "benevolence", "courtesy", "wisdom", "honesty", "respect"];
    const [scores, setScores] = useState<Array<number>>([10, 10, 10, 10, 10, 10]);

    const getNextQuestion = (chosen: string | null) => {
        if (questionCount == maxQuestionCount + 1) {
            propagateState("ok");
            setGameOver(true);
            return;
        }
        let previous_question = "";
        let previous_response = "";
        if (chosen !== null && currentQuestion !== null) {
            previous_question = currentQuestion.question_text;
            previous_response = chosen;
        }

        axios.post("https://porygon.andrewli.org/twine/prompt", {
            "previous_question": previous_question,
            "previous_response": previous_response,
        })
            .then((res) => res.data)
            .then((data) => {
                setCurrentQuestion(data);
            })
            .catch((_) => {
                setCurrentQuestion({question_text: "Unfortunately, you might have to restart due to an error.", responses: []}); 
            });
    }

    const processResponse = (text: string, s: Array<number>) => {
        setQuestionCount(questionCount + 1);
        let old_scores = scores.slice();
        for (let i = 0; i < s.length; i ++) {
            old_scores[i] += s[i];
            if (old_scores[i] > 20) {
                old_scores[i] = 20;
            }
            if (old_scores[i] <= 0) {
                propagateState("Game over! You've failed to maintain a balance of all six scores.");
            }
        }
        setScores(old_scores);
        getNextQuestion(text);
        setCurrentQuestion(null);
    }

    const getColor = (score: number) => {
        if (score <= 5) {
            return "red"
        } else if (score <= 7.5) {
            return "orange"
        } else if (score <= 15) {
            return "yellow"
        } else {
            return "green"
        }
    }

    useEffect(() => {
        getNextQuestion(null);
    }, []);

    if (gameOver) {
        return (
            <div>
                <div>It's time to land soon. Maybe it's time to start packing your things instead of talking to this weirdo.</div>
            </div>
        );
    }

    if (currentQuestion === null) {
        return (
            <div className="the_game">
                <div className="question">Loading question...</div>
    
                <div className="response_c">Loading responses...</div>

                <div className="stats">
                    {scores.map((score, index) => (
                        <div style={{margin: "0.25rem", display: "flex", flexDirection: "row", gap: "0.5rem"}}>
                            <div>{scoreLabels[index]}</div>
                            <div style={{width: `${score*10}px`, backgroundColor: getColor(score)}}></div>
                            <div>{score}/25</div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className="the_game">
            <div className="question">{questionCount + 1}/{maxQuestionCount} {currentQuestion.question_text}</div>

            {currentQuestion.responses.map((response, index) => (
                <div key={`question_${index}`} className="response" onClick={() => {
                    processResponse(response.response_text, response.scores);
                }}>{response.response_text}</div>
            ))}

                <div className="stats">
                    {scores.map((score, index) => (
                        <div style={{margin: "0.25rem", display: "flex", flexDirection: "row", gap: "0.5rem"}}>
                            <div>{scoreLabels[index]}</div>
                            <div style={{width: `${score*10}px`, backgroundColor: getColor(score)}}></div>
                            <div>{score}/25</div>
                        </div>
                    ))}
                </div>
        </div>
    );
};

export default TheGame;
