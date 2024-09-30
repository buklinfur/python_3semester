# matrices management functions
def read_matrix(file_name: str): 
    fin = open(file_name, 'r')
    lines = fin.read().split('\n')
    matrix = [[int(num) for num in line.split(' ') if num != ''] for line in lines]
    fin.close()
    return matrix

def write_matrix(matrix): 
    lines = [' '.join([str(digit) for digit in line]) for line in matrix]
    text = '\n'.join(lines)
    print(text)

def read_matrices(): 
    print('File name 1: ')
    filename1 = input()
    print('File name 2: ')
    filename2 = input()
    matrix1 = read_matrix(filename1)
    matrix2 = read_matrix(filename2)
    return matrix1, matrix2

def sumMatrices(matrix1, matrix2):
    matrix_res = []
    for i in range(len(matrix1)):
        matrix_res.append([])
        for j in range(len(matrix1[0])):
            matrix_res[i].append(matrix1[i][j] + matrix2[i][j])
    return matrix_res

def subMatrices(matrix1, matrix2):
    matrix_res = []
    for i in range(len(matrix1)):
        matrix_res.append([])
        for j in range(len(matrix1[0])):
            matrix_res[i].append(matrix1[i][j] - matrix2[i][j])
    return matrix_res

# general employee class for abstract no-type employee
class Employee:
    def __init__(self, name: str):
        self.name = name
        self.balance = 0.
    
    def take_salary (self, salary: float):
        self.balance += salary

    def do_work (self):
        raise Exception ("Abstract employee can't do work")

    def get_balance (self):
        print(f"Employee: {self.name}\nBalance:{self.balance}\n")

# pupa-type employee class
class Pupa (Employee):
    def __init__(self, name: str):
        super().__init__(name = name)

    def do_work(self):
        matrix1, matrix2 = read_matrices()
        write_matrix(sumMatrices(matrix1, matrix2))

# lupa-type employee class
class Lupa (Employee):
    def __init__(self, name: str):
        super().__init__(name = name)

    def do_work(self):
        matrix1, matrix2 = read_matrices()
        write_matrix(subMatrices(matrix1, matrix2))

# manager class for employment operations
class EmploymentManager:
    employee_by_name = {}
    grade_by_employee_name = {}

    @staticmethod
    def employ(employee: Employee, salary: float):
        EmploymentManager.employee_by_name[employee.name] = employee
        EmploymentManager.grade_by_employee_name[employee.name] = salary

    @staticmethod
    def get_employee(name: str):
        return EmploymentManager.employee_by_name[name]
    
    @staticmethod
    def get_all_employees():
        return [e for e in EmploymentManager.employee_by_name.values()]

    @staticmethod
    def get_grade(name: str):
        return EmploymentManager.grade_by_employee_name[name]
    
# accountant-type employee class
class Accountant (Employee):
    def __init__(self, name: str):
        super().__init__(name = name)
        self.authorised_transactions = []

    def give_salary(self, name:str):
        employee = EmploymentManager.get_employee(name)
        grade = EmploymentManager.get_grade(name)
        employee.take_salary(grade)
        self.authorised_transactions.append((name, grade))

    def do_work(self):
        for employee in EmploymentManager.get_all_employees():
            self.give_salary(employee.name)

class Employment:
    @staticmethod
    def create_employee(employee_type: str, name: str) -> Employee:
        if employee_type.lower() == 'pupa':
            employee = Pupa(name)
        elif employee_type.lower() == 'lupa':
            employee = Lupa(name)
        elif employee_type.lower() == 'accountant':
            employee = Accountant(name)
        else:
            raise Exception('Unknown employee type')
        return employee

def main ():
    pupa1 = Employment.create_employee('pupa', 'pupa1')
    EmploymentManager.employ(pupa1, 228)
    lupa1 = Employment.create_employee('lupa', 'lupa1')
    EmploymentManager.employ(lupa1, 282)

    accountant1 = Employment.create_employee('accountant', 'accountant1')
    EmploymentManager.employ(accountant1, 1337)

    for employee in EmploymentManager.get_all_employees():
        employee.do_work()

    for employee in EmploymentManager.get_all_employees():
        employee.get_balance()

main()