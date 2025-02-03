import AnimatePage from "./AnimatePage";

interface IPage {
    propagateState: (b: boolean) => void
}

export const Warnings: React.FC<IPage> = ({propagateState}) => {
    return (
        <AnimatePage propagateState={(b: boolean) => {
            propagateState(b);
        }}>
            <p style={{fontWeight: 700}}>Don't refresh or leave this page. You will lose your progress.</p>
        </AnimatePage>
    );
};

export const PageTwo: React.FC<IPage> = ({propagateState}) => {
    return (
        <AnimatePage propagateState={(b: boolean) => {
            propagateState(b);
        }}>
            <p style={{fontWeight: 700}}><em>December 2023</em></p>
            <p>You're at Minneapolis St. Paul International Airport, on the way home for Winter Break.</p>
            <p>Where's home for you?</p>
            <p>Maybe you have one answer? Or maybe you have five.</p>
            <p>It's a personal question; one with personal answers.</p>
            <p>Some people just want to know <em>everything</em>.</p>
        </AnimatePage>
    )
}

export const PageThree: React.FC<IPage> = ({propagateState}) => {
    return (
        <AnimatePage propagateState={(b: boolean) => {
            propagateState(b);
        }}>
            <p>It's time to board your flight to Somewhere, Someplace, Somecountry.</p>
            <p>You just want to fly in peace; maybe look out the window a little, maybe sleep, and maybe eat.</p>
            <p>After settling in, you submit your last assignment of the quarter: some extra credit.</p>
            <p>A voice. It's your seatmate sitting in the aisle seat.</p>
            <p>A tall white man who looks carefree is siting inches away from you and it seems that he wants to talk to you.</p>
        </AnimatePage>
    )
};

export const TheRules: React.FC<IPage> = ({propagateState}) => {
    return (
        <AnimatePage propagateState={(b: boolean) => {
            propagateState(b);
        }}>
            <p style={{fontWeight: 700}}>Don't let your scores reach zero. Or else.</p>
        </AnimatePage>
    );
};

export const EndingScreen: React.FC<IPage> = ({propagateState}) => {
    return (
        <AnimatePage propagateState={(b: boolean) => {
            propagateState(b);
        }}>
            <p style={{fontWeight: 700}}>Well, the game is now over. Did you win? Maybe you lost.</p>
            <p>But what does it even mean to win in a game like this?</p>
            <p>Is winning truly possible?</p>
            <p><em>Should</em> winning be possible?</p>
        </AnimatePage>
    );
};

export const Credits: React.FC<IPage> = ({propagateState}) => {
    return (
        <AnimatePage propagateState={(b: boolean) => {
            propagateState(b);
        }}>
            <p style={{fontWeight: 700}}>Credits</p>
            <p>Programming and Design: Andrew Li</p>
            <p>The Class: Professor Tara Fickle</p>
        </AnimatePage>
    );
};
