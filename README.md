# just_wordle
A terminal-based Wordle clone with some extra customization options.

## Features
By default, includes 5-, 6-, and 7-letter Wordle. More word lengths can be added by simply adding solution files following this naming convention: "solutions_N.txt" for N-letter words.

**Two game modes: normal and evil.** Normal mode follows the same rules as the official game. Evil mode comes with a twist: the engine is cheating! Instead of picking a word at the start of the game and sticking to it, it evaluates its remaining possibilities after each guess and returns the color pattern that keeps the most words still in play - with some weighted randomness to keep the gameplay fun.

**Two difficulty settings: normal and hard.** Normal difficulty is standard Wordle. Hard mode adds another twist: you can only make guesses that are consistent with the feedback from your previous guesses. For example, if you guessed "horse" and the H was green, all subsequent guesses must start with H.

**Customizable guess limit:** Choose anywhere from 1 to 12 guesses per game, or set it to infinite.

## Requirements
- Python 3.13 or later
- uv: [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/sQnteri/just_wordle.git
```
2. Navigate to the project directory:
```bash
cd just_wordle
```
3. Install dependencies:
```bash
uv sync
```
4. Generate the word lists:
```bash
uv run setup
```
5. Run the game:
```bash
uv run wordle
```