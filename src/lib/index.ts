import {checkWithProfanity} from "./checkWithProfanity";
import {checkWithBadWordsNext} from "./checkWithBadWordsNext";


export const checkProfanity = (text: string) => {
    return checkWithProfanity(text) || checkWithBadWordsNext(text)
}