import BadWordsNext from "bad-words-next";
import bad_words_en from "bad-words-next/data/en.json";
import bad_words_de from "bad-words-next/data/de.json";

const badwords = new BadWordsNext()
badwords.add(bad_words_en)
badwords.add(bad_words_de)

console.log('Custom words added to bad-words-next library')

export const checkWithBadWordsNext = (text: string) => {

    const normalizedText = text.toLowerCase().replace(/\s+/g, ' ')

    return badwords.check(normalizedText)
}