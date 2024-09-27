from .SentimentAnalysisFacade import SentimentAnalysisFacade

class SentimentAnalysisApplication:
    @staticmethod 
    def main():
        facade = SentimentAnalysisFacade()
        exit_application = False 

        while not exit_application:
            print("\nWelcome to the Sentiment Analyzer")
            print("1. Show Description of Sentiment Analysis Methods")
            print("2. Select Sentiment Analysis Method")
            print("3. Analyze Text")
            print("4. Save Analysis")
            print("5. Restore Analysis")
            print("6. Exit")
            print("\nPlease enter your choice: ")

            choice = input()

            if choice == "1":
                facade.show_description()
            elif choice == "2":
                print("\nSelect a sentiment analyzer (basic/advanced)")
                analyzer_choice = input()
                facade.select_analyzer(analyzer_choice)
            elif choice == "3":
                print("\nEnter text to analyze:")
                input_text = input()
                facade.analyze_text(input_text)
            elif choice == "4":
                facade.save_analysis()
            elif choice == "5":
                facade.restore_analysis()
            elif choice == "6":
                exit_application = True
                print("\nExiting the application.")
            else:
                print("Invalid choice, please try again.") 

if __name__ == "__main__":
    SentimentAnalysisApplication.main()

