from pipelines.pipeline import run_research_pipeline

def main():
    topic = input("Enter a topic: ")

    result = run_research_pipeline(topic)

if __name__ == "__main__":
    main()
    