import { Button } from "@mantine/core";
import { ReactNode, useState } from "react"

export const AnimatePage: React.FC<{ children: ReactNode, propagateState: (b: boolean) => void }> = ({children, propagateState}) => {
    const [frameNumber, setFrameNumber] = useState(0);
    const [showButton, setShowButton] = useState(true);

    if (!Array.isArray(children)) {
        propagateState(true);
        return <div>
            {children}
        </div>;
    }

    let cArray: Array<ReactNode> = children;

    return <div>
        {cArray.slice(0, frameNumber + 1)}
        {showButton && <Button onClick={() => {
            setFrameNumber(frameNumber + 1);
            if (frameNumber + 1 == cArray.length - 1) {
                setShowButton(false);
                propagateState(true);
                return;
            }
        }}>Continue</Button>}
    </div>
}

export default AnimatePage;

