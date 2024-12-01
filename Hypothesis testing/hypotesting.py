import pandas as pd
import seaborn as sns
import numpy as np
class HypoTestFunctions:
    def __init__(self):
        self.choice = None
        self.choice = None
        # self.df =  None
        self.available_data = None
        self.user_choice()
        self.get_valid_test()

    def user_choice(self):
        print("Select the Dataset type below:!")
        self.choice = input("Seaborn dataset library or CSV file?:\n").lower()
        if self.choice in ["seaborn" or "sns"]:
            self.seaborn()
            self.user_choice()
        elif self.choice in ["csv", "csvfile"]:
            self.reading_file()
        else:
            print(f"Please Enter a Valid File Source")
            self.user_choice()


    def seaborn(self):
        self.available_data = sns.get_dataset_names()
        print(f"DataSets\n{self.available_data}")
        while True:
            self.choice = input("Enter the dataset you want to get load from seaborn:\n").lower()

            if self.choice in self.available_data:
                self.df = sns.load_dataset(self.choice)
                print(self.df)
                print(self.df.info())
                break
            else:
                print(f"Dataset not found named: {self.choice}. invalid request!")
                continue
        self.get_valid_test()

    def reading_file(self):

        self.choice = input("Enter only CSV file name with or without Extension, your wish:\n")
        print("Available_datasets\n",self.available_data)
        if not self.choice.endswith(".csv"):
            self.choice += ".csv"
        try:
            #to open the file to check existence

            with open(self.choice, 'r') as file:
                self.available_data = pd.read_csv(self.choice)
                self.df = pd.read_csv(self.choice)
                print(f"File found: {self.choice}")
                print(f"{self.choice} is loaded")
                print(self.available_data)
                print(self.df.info())

        except FileNotFoundError:
            print()
            print(f"Error: File '{self.choice}' not found. Please try again.")
            self.reading_file()
            self.df = pd.read_csv(self.choice)
            print(self.choice)
            print(self.df)
            self.df.info()


    def get_valid_test(self):
        while True:
            print()
            # print("Dataset", self.available_data)
            print("Available tests\n['chisquare', 'ftest'] Enter below as seen:!" )
            choice = input(f"Enter test you want to perform on {self.choice} or tpye No to select another file or dataset:\n").lower()

            if choice in ["chisquare", "chi2", "chi"]:
                self.chisquare_test()
            elif choice in ["ftest", "f-test", "f"]:
                self.f_test()
            elif choice == "no":
                self.__init__()
            elif choice == "exit":
                print("Thank you for testing the program")
                break
            else:
                self.get_valid_test()

    def get_valid_dataset(self):
        while True:
            self.choice = input("Enter the dataset you want to get load from seaborn:\n").lower()

            if self.choice in self.available_data:
                self.df = sns.load_dataset(self.choice)
                print(self.df)
                break
            else:
                print(f"Dataset not found named: {self.choice}. invalid request!")




    def chisquare_test(self):
        """This function is for performing Chi-Square_testing with all the datasets which
        It also handles numerical by converting it not categorical
        """
        while True:

            select_first_column = input("Enter First Categorical group from the dataset:\n")
            select_second_column = input("Enter Second Categorical group from the dataset:\n")

            if select_first_column not in self.df.columns or select_second_column not in self.df.columns:
                print("One or both columns not found in the dataset. Please check column names.")
                continue

            if not pd.api.types.is_categorical_dtype(self.df[select_first_column]):
                self.df[select_first_column] = self.df[select_first_column].astype("category")

            if not pd.api.types.is_categorical_dtype(self.df[select_second_column]):
                self.df[select_second_column] = self.df[select_second_column].astype("category")

            # checking again after conversion
            if not pd.api.types.is_categorical_dtype(self.df[select_first_column]) or \
                    not pd.api.types.is_categorical_dtype(self.df[select_second_column]):
                print("Both columns must be categorical. Please try again")
                continue

            print("Summary of those two groups")
            data_table = pd.crosstab(self.df[select_first_column], self.df[select_second_column])
            print(data_table)
            print()
            observed_values = data_table.values
            print(f"observed value\n{observed_values}\n")
            print()
            import scipy.stats as stats
            stats_test, p, dof, expected_values = stats.chi2_contingency(observed_values)
            print(f"P-value from chi2_contingency test: {p}\n")
            print()
            print(f"expected_values\n{expected_values}\n")
            print()
            # importing Chi-Square library for calculating critical value
            from scipy.stats import chi2
            rows, columns = observed_values.shape
            # Performing chi-square test manually
            # chi_square_test = sum([(0 - e) ** 2 / e for o, e in zip(observed_values.flatten(), expected_values.flatten())])
            print(f"chi-square-Test is: {stats_test}")
            print()
            chi_square_stats = stats_test
            print(f"The Chi-Square-Stats is: {chi_square_stats}\n")
            print()
            dof = (rows - 1) * (columns - 1)
            chi_square_critical = chi2.ppf(1 - 0.05, dof)
            print(f"Chi-Square-Critical is: {chi_square_critical}")
            print()
            if chi_square_stats >= chi_square_critical:
                print(f"Chi-square-stats {chi_square_stats} >= Chi-Square-critical {chi_square_critical}")
                print("Reject the Null Hypothesis (Ho)")
                print()
            else:
                print("Fail to reject the Null Hypothesis")
                print()
            break
        self.get_valid_test()



    def f_test(self):
        """
        This function do the f-test
        It does not handles categorical data ill surely convert it when next time open up he program
        :return:
        """
        print("Comparing Two variances")
        while True:
            first_group = input("Enter first numerical column:\n")
            second_group = input("Enter second numerical column:\n")
            if not first_group.strip() or not second_group.strip():
                print("Input columns cannot be empty.")
                continue

            if first_group not in self.df.columns or second_group not in self.df.columns:
                print("Please a valid Numerical Columns")
                continue
            # for first column
            # Ensuring the first column is numeric
            first_group_data = pd.to_numeric(self.df[first_group], errors='coerce')
            first_group_data = first_group_data.dropna()

            # ensuring the second column is numeric
            second_group_data = pd.to_numeric(self.df[second_group], errors='coerce')
            second_group_data = second_group_data.dropna()

            if len(first_group_data) == 0 or len(second_group_data) == 0:
                print("One of the columns has no valid numerical data after conversion.")
                continue
            else:
                f_stats = np.var(first_group_data, ddof=1) / np.var(second_group_data, ddof=1)
                print(f"F-statistic is: {f_stats}")
                degree_freedom1 = len(first_group_data) - 1
                degree_freedom2 = len(second_group_data) - 1
                # Critical value
                from scipy.stats import f
                critical_value = f.ppf(q=1 - 0.05, dfn=degree_freedom1, dfd=degree_freedom2)
                print(f"Critical Value is {critical_value}")
                if f_stats > critical_value:
                    print("Reject the Null Hypothesis")
                    print(f"F-Statistics is greater the F-Critical")
                else:
                    print(f"F-Critical is greater the F-Statistics")
                    print("Fail to reject the null Hypothesis")
                break
        self.get_valid_test()