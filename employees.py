from ZODB import FileStorage, DB, persistentclass
import persistent
import transaction

class Employee(persistent.Persistent):
    """An employee"""

    def __init__(self, name, manager=None):
        self.name=name
        self.manager=manager

# setup the database
storage=FileStorage.FileStorage("employees.fs")
db=DB(storage)
connection=db.open()
root=connection.root()

# get the employees mapping, creating an empty mapping if necessary
if "employees" not in root:
    root["employees"] = {}
employees=root["employees"]

def listEmployees():
    if len(employees.values())==0:
        print ("There are no employees.")
        print
        return
    for employee in employees.values():
        if employee.manager is not None:
            print ("Name: {} (Manager: {})".format(employee.name, employee.manager.name))
        else:
            print ("Name: %s" % employee.name)
        print

def addEmployee(name, manager_name=None):
    if name in employees:
        print ("There is already an employee with this name.")
        return
    if manager_name:
        try:
            manager=employees[manager_name]
        except KeyError:
            print
            print ("No such manager")
            print
            return
        employees[name]=Employee(name, manager)
    else:
        employees[name]=Employee(name)

    root['employees'] = employees  # reassign to change
    transaction.commit()
    print ("Employee %s added." % name)
    print

if __name__=="__main__":
    while 1:
        choice=input("Choose 'L' to list employees, 'A' to add an employee, or 'Q' to quit:")
        choice=choice.lower()
        if choice=="l":
            listEmployees()
        elif choice=="a":
            name=input("Employee name:")
            manager_name=input("Manager name:")
            addEmployee(name, manager_name)
        elif choice=="q":
            break

    # close database
    connection.close()