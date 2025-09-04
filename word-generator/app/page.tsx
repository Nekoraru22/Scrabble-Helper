"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"

export default function WordGenerator() {
  const [inputWord, setInputWord] = useState("")
  const [count, setCount] = useState<number>(5)
  const [generatedWords, setGeneratedWords] = useState<string[]>([])

  const generateWords = () => {
    if (!inputWord.trim()) return

    const word = inputWord.trim().toLowerCase()
    const words: string[] = []

    // Generate word variations
    const prefixes = ["un", "re", "pre", "over", "under", "out", "up"]
    const suffixes = ["ing", "ed", "er", "est", "ly", "ness", "ful", "less"]

    // Add the original word
    words.push(word)

    // Add prefixed versions
    for (const prefix of prefixes) {
      if (words.length >= count) break
      words.push(prefix + word)
    }

    // Add suffixed versions
    for (const suffix of suffixes) {
      if (words.length >= count) break
      words.push(word + suffix)
    }

    // Add some simple rhyming patterns
    const rhymeEndings = ["at", "ing", "tion", "ly", "er"]
    for (const ending of rhymeEndings) {
      if (words.length >= count) break
      const baseWord = word.slice(0, -2) || word
      words.push(baseWord + ending)
    }

    // Ensure we have exactly the requested count
    setGeneratedWords(words.slice(0, count))
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md p-8 space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-semibold text-foreground">Word Generator</h1>
          <p className="text-sm text-muted-foreground">Enter a word and number to generate variations</p>
        </div>

        <div className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="word" className="text-sm font-medium text-foreground">
              Word
            </label>
            <Input
              id="word"
              type="text"
              placeholder="Enter a word..."
              value={inputWord}
              onChange={(e) => setInputWord(e.target.value)}
              className="w-full"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="count" className="text-sm font-medium text-foreground">
              Number of words
            </label>
            <Input
              id="count"
              type="number"
              min="1"
              max="20"
              value={count}
              onChange={(e) => setCount(Number.parseInt(e.target.value) || 1)}
              className="w-full"
            />
          </div>

          <Button onClick={generateWords} className="w-full" disabled={!inputWord.trim()}>
            Generate Words
          </Button>
        </div>

        {generatedWords.length > 0 && (
          <div className="space-y-3">
            <h2 className="text-lg font-medium text-foreground">Generated Words</h2>
            <div className="space-y-2">
              {generatedWords.map((word, index) => (
                <div key={index} className="p-3 bg-muted rounded-md text-sm text-foreground">
                  {word}
                </div>
              ))}
            </div>
          </div>
        )}
      </Card>
    </div>
  )
}
