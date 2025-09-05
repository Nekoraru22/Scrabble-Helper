"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface WordResult {
  is_bloque: boolean
  length: number
  value: string
}

export default function WordGenerator() {
  const [inputWord, setInputWord] = useState("")
  const [count, setCount] = useState<number>(0)
  const [orMore, setOrMore] = useState<boolean>(false)
  const [generatedWords, setGeneratedWords] = useState<WordResult[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [firstLoad, setFirstLoad] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const generateWords = async () => {
    if (!inputWord.trim()) return

    if (firstLoad) setFirstLoad(false)
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(`/search/${encodeURIComponent(inputWord.trim())}/${count}?or_more=${orMore}`)

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const words = await response.json()
      setGeneratedWords(Array.isArray(words) ? words : [])
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch words")
      setGeneratedWords([])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900 relative overflow-hidden flex items-center justify-center p-4">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-1/2 -right-1/2 w-96 h-96 bg-gradient-to-br from-blue-200/30 to-purple-200/30 dark:from-blue-900/20 dark:to-purple-900/20 rounded-full blur-3xl animate-pulse"></div>
          <div
            className="absolute -bottom-1/2 -left-1/2 w-96 h-96 bg-gradient-to-tr from-indigo-200/30 to-pink-200/30 dark:from-indigo-900/20 dark:to-pink-900/20 rounded-full blur-3xl animate-pulse"
            style={{ animationDelay: "2s" }}
          ></div>
          <div
            className="absolute top-1/4 left-1/4 w-32 h-32 bg-gradient-to-br from-yellow-200/20 to-orange-200/20 dark:from-yellow-900/10 dark:to-orange-900/10 rounded-full blur-2xl animate-bounce"
            style={{ animationDuration: "3s" }}
          ></div>
        </div>

        <Card className="w-full max-w-md p-8 space-y-6 bg-white/80 dark:bg-slate-800/80 backdrop-blur-lg border border-white/20 dark:border-slate-700/50 shadow-2xl">
          <div className="flex justify-center mb-6">
            <img src="/rete.png" alt="rete" className="w-52" />
          </div>

          <div className="text-center space-y-2">
            <h1 className="text-2xl font-semibold text-foreground">Scrabble Helper</h1>
            <p className="text-sm text-muted-foreground">Enter a word and number of letters to search for words</p>
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
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    generateWords()
                  }
                }}
                className="w-full bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm border-white/30 dark:border-slate-600/30"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="count" className="text-sm font-medium text-foreground">
                Number of letters
              </label>
              <div className="flex items-center space-x-3">
                <Input
                  id="count"
                  type="number"
                  min="0"
                  max="20"
                  value={count}
                  onChange={(e) => setCount(Number.parseInt(e.target.value) || 0)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      generateWords()
                    }
                  }}
                  className="flex-1 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm border-white/30 dark:border-slate-600/30"
                />
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="orMore"
                    checked={orMore}
                    onChange={(e) => setOrMore(e.target.checked)}
                    className="w-4 h-4 text-blue-600 bg-white/50 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <label htmlFor="orMore" className="text-sm font-medium text-foreground whitespace-nowrap">
                    or more
                  </label>
                </div>
              </div>
            </div>

            <Button
              onClick={generateWords}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-[1.02]"
              disabled={!inputWord.trim() || isLoading}
            >
              {isLoading ? (
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Searching...</span>
                </div>
              ) : (
                "Search Words"
              )}
            </Button>
          </div>

          {error && (
            <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800/30 rounded-md backdrop-blur-sm">
              <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
            </div>
          )}

          {generatedWords.length > 0 && (
            <div className="space-y-3">
              <h2 className="text-lg font-medium text-foreground">Found Words ({generatedWords.length})</h2>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {generatedWords.map((wordObj) => (
                  <div
                    key={wordObj.value}
                    className={`p-3 rounded-md text-sm text-foreground backdrop-blur-sm transition-shadow duration-200 ${
                      wordObj.is_bloque
                        ? "bg-red-50 dark:bg-red-900/20 border-2 border-red-500 dark:border-red-400 hover:shadow-md"
                        : "bg-gradient-to-r from-blue-50 to-purple-50 dark:from-slate-700/50 dark:to-slate-600/50 border border-white/20 dark:border-slate-600/20 hover:shadow-md"
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-medium">{wordObj.value}</span>
                      <span className="text-xs text-muted-foreground">
                        {wordObj.length} letters
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {generatedWords.length === 0 && !firstLoad && !isLoading && !error && (
            <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800/30 rounded-md backdrop-blur-sm">
              <p className="text-sm text-yellow-700 dark:text-yellow-300">No words found. Try a different input.</p>
            </div>
          )}
        </Card>

        <div className="fixed bottom-6 right-6 z-10">
          <Tooltip>
            <TooltipTrigger asChild>
              <button
                type="button"
                className="cursor-pointer hover:scale-105 transition-transform duration-200 bg-transparent border-none p-0"
                onClick={() => window.open("https://github.com/Nekoraru22", "_blank")}
                aria-label="Open creator's website"
              >
                <img src="/neko.png" alt="neko" className="w-48 object-contain drop-shadow-lg" />
              </button>
            </TooltipTrigger>
            <TooltipContent
              side="left"
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white border-none shadow-xl"
            >
              <p className="font-medium">✨ Neko te odia! ✨</p>
              <p className="text-xs opacity-90">Meow :3</p>
            </TooltipContent>
          </Tooltip>
        </div>
      </div>
    </TooltipProvider>
  )
}