import {Profanity, ProfanityOptions} from '@2toad/profanity';
import {bad_words_de} from "@/recources/bad_words_de";
import {bad_words_en} from "@/recources/bad_words_en";

const options = new ProfanityOptions()
options.wholeWord = false
options.grawlix = '*****'
options.grawlixChar = '*'

const customProfanity = new Profanity(options)

customProfanity.addWords(bad_words_de)
customProfanity.addWords(bad_words_en)
console.log('Custom words added to profanity library')

export const checkWithProfanity = (text: string) => {

    const normalizedText = text.toLowerCase().replace(/\s+/g, '')

    return customProfanity.exists(normalizedText)
}