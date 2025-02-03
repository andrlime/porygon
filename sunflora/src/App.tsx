import './App.css'

import { useState } from 'react'

import { Credits, EndingScreen, PageThree, PageTwo, TheRules, Warnings } from './components/pages'
import { Button } from '@mantine/core'
import TheGame from './components/TheGame';

function App() {
  const [pageIndex, setPageIndex] = useState(0);
  const [toContinue, setToContinue] = useState(false);
  const [gameOverMessage, setGameOverMessage] = useState("");

  const pages = [
    <Warnings propagateState={setToContinue} />,
    <PageTwo propagateState={setToContinue} />,
    <PageThree propagateState={setToContinue} />,
    <TheRules propagateState={setToContinue} />,
    <TheGame propagateState={(s: string) => {
      if (s === "ok") {
        setToContinue(true);
        return;
      }
      setGameOverMessage(s);
    }} maxQuestionCount={10} />,
    <EndingScreen propagateState={setToContinue} />,
    <Credits propagateState={(_: boolean) => {}} />
  ]

  if (gameOverMessage !== "") {
    return (
      <div>
        <p>{gameOverMessage}</p>
        <Button onClick={() => {
          if (pageIndex + 1 == pages.length) return;
          setGameOverMessage("");
          setPageIndex(pageIndex + 1);
          setToContinue(false);
        }}>Next</Button>
      </div>
    );
  }

  return (
    <div>
      {pages[pageIndex]}
      {toContinue && <Button onClick={() => {
        if (pageIndex + 1 == pages.length) return;
        setPageIndex(pageIndex + 1);
        setToContinue(false);
      }}>Next</Button>}
    </div>
  )
}

export default App
