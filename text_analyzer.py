
import re
import sys
from collections import Counter

STOPWORDS = set("""
a an the and or but if then else of to in on at for with by from as is are was were be been being
this that these those it its i we you he she they them his her our your their my me us not no so
very just also than too can could would should will shall may might do does did have has had
there here what which who whom when where why how all any both each few more most other some such
only own same into over under again about after before out up down off above below between
""".split())

POSITIVE = set("""
good great excellent amazing awesome fantastic wonderful love loved like liked best happy pleased
fast quick smooth easy friendly helpful beautiful perfect recommend recommended reliable impressive
comfortable delicious clean nice brilliant superb enjoy enjoyed
""".split())

NEGATIVE = set("""
bad poor terrible awful horrible worst hate hated slow late broken rude dirty difficult hard
disappointing disappointed useless expensive noisy buggy faulty problem problems issue issues
waste refund complaint uncomfortable cold stale never failed fails crash crashed
""".split())

NEGATIONS = {
    "not", "no", "never", "hardly", "isn't", "wasn't",
    "don't", "didn't", "can't", "won't"
}

MONTHS = (
    "January|February|March|April|May|June|July|August|"
    "September|October|November|December"
)

SENTENCE_STARTERS = {
    "The", "A", "An", "It", "This", "That", "I", "We",
    "They", "He", "She", "My", "Our", "But", "And",
    "So", "If", "When", "However", "In", "On", "At",
    "After", "Before", "Ask"
}


def tokenize(text):
    return re.findall(r"[A-Za-z']+", text.lower())


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


# 1. Keyword Extraction
def extract_keywords(text, top_n=8):
    words = [
        word for word in tokenize(text)
        if word not in STOPWORDS and len(word) > 2
    ]
    return Counter(words).most_common(top_n)


# 2. Entity Detection
def detect_entities(text):
    entities = []

    emails = re.findall(
        r"[\w.+-]+@[\w-]+\.[\w.]+", text
    )
    for item in emails:
        entities.append((item, "Email"))

    urls = re.findall(r"https?://\S+", text)
    for item in urls:
        entities.append((item.rstrip(".,"), "URL"))

    money = re.findall(
        r"(?:Rs\.?|INR|\$|₹)\s?\d+(?:,\d{3})*(?:\.\d+)?",
        text
    )
    for item in money:
        entities.append((item, "Money"))

    dates = re.findall(
        rf"\b(?:\d{{1,2}}\s)?(?:{MONTHS})"
        r"(?:\s\d{1,2})?(?:,?\s\d{4})?\b",
        text
    )
    for item in dates:
        entities.append((item.strip(), "Date"))

    # Detect names and places
    for sentence in split_sentences(text):
        words = sentence.split()
        i = 0

        while i < len(words):
            word = words[i].strip(".,!?;:\"'()")

            if (
                word[:1].isupper()
                and word not in SENTENCE_STARTERS
                and word not in MONTHS.split("|")
                and word.isalpha()
            ):
                chunk = [word]
                j = i + 1

                while j < len(words):
                    next_word = words[j].strip(
                        ".,!?;:\"'()"
                    )

                    if (
                        next_word[:1].isupper()
                        and next_word.isalpha()
                    ):
                        chunk.append(next_word)
                        j += 1
                    else:
                        break

                entities.append(
                    (" ".join(chunk), "Name/Place/Org")
                )
                i = j

            else:
                i += 1

    unique_entities = []
    seen = set()

    for entity in entities:
        if entity not in seen:
            seen.add(entity)
            unique_entities.append(entity)

    return unique_entities


# 3. Sentiment Analysis
def sentence_sentiment(sentence):
    words = tokenize(sentence)
    score = 0

    for i, word in enumerate(words):
        if word in POSITIVE:
            value = 1
        elif word in NEGATIVE:
            value = -1
        else:
            value = 0

        if (
            value != 0
            and i > 0
            and words[i - 1] in NEGATIONS
        ):
            value = -value

        score += value

    return score


def analyze_sentiment(text):
    sentences = split_sentences(text)

    positive = 0
    negative = 0
    neutral = 0
    sentence_results = []

    for sentence in sentences:
        score = sentence_sentiment(sentence)

        if score > 0:
            label = "positive"
            positive += 1
        elif score < 0:
            label = "negative"
            negative += 1
        else:
            label = "neutral"
            neutral += 1

        sentence_results.append((sentence, label))

    total = max(len(sentences), 1)

    if positive > negative:
        overall = "positive"
    elif negative > positive:
        overall = "negative"
    elif positive > 0 and negative > 0:
        overall = "mixed"
    else:
        overall = "neutral"

    scores = {
        "positive": round(positive / total, 2),
        "neutral": round(neutral / total, 2),
        "negative": round(negative / total, 2)
    }

    return overall, scores, sentence_results


# 4. Text Summarization
def summarize(text, num_sentences=2):
    sentences = split_sentences(text)

    if len(sentences) <= num_sentences:
        return " ".join(sentences)

    frequencies = dict(
        extract_keywords(text, top_n=50)
    )

    scored_sentences = []

    for index, sentence in enumerate(sentences):
        words = [
            word for word in tokenize(sentence)
            if word in frequencies
        ]

        score = sum(
            frequencies[word] for word in words
        ) / (len(tokenize(sentence)) ** 0.5 or 1)

        scored_sentences.append(
            (score, index, sentence)
        )

    selected = sorted(
        scored_sentences,
        key=lambda item: item[0],
        reverse=True
    )[:num_sentences]

    selected.sort(key=lambda item: item[1])

    return " ".join(
        sentence for _, _, sentence in selected
    )


# Complete Analysis
def analyze(text):
    overall, scores, sentence_results = analyze_sentiment(text)

    return {
        "keywords": extract_keywords(text),
        "entities": detect_entities(text),
        "sentiment": overall,
        "sentiment_scores": scores,
        "sentence_sentiments": sentence_results,
        "summary": summarize(text)
    }


# Display Analysis Report
def print_report(title, text):
    result = analyze(text)

    print("=" * 70)
    print(title)
    print("=" * 70)

    print("\nKeywords:")
    for word, count in result["keywords"]:
        print(f"{word}: {count}")

    print("\nEntities:")
    for entity, category in result["entities"]:
        print(f"{entity} [{category}]")

    print("\nOverall Sentiment:")
    print(result["sentiment"])

    print("\nSentiment Scores:")
    print(result["sentiment_scores"])

    print("\nSentence-wise Sentiment:")
    for sentence, sentiment in result["sentence_sentiments"]:
        print(f"{sentiment}: {sentence}")

    print("\nSummary:")
    print(result["summary"])
    print()


# Main Program
if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(
            sys.argv[1], "r", encoding="utf-8"
        ) as file:
            text = file.read()

        print_report("Text Analysis Report", text)

    else:
        print("Smart Review Analyzer")
        print("Usage: python text_analyzer.py filename.txt")
        print("Or run: python demo.py")
