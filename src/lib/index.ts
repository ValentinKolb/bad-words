import {checkWithProfanity} from "@/lib/checkWithProfanity";
import {checkWithBadWordsNext} from "@/lib/checkWithBadWordsNext";


export const checkProfanity = (text: string) => {
    return checkWithProfanity(text) || checkWithBadWordsNext(text)
}