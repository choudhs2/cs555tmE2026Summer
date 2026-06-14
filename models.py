from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

class Individual:
    def __init__(self, indi_id):
        self.id = indi_id
        self.name = "NA"
        self.gender = "NA"
        self.birthday = None
        self.death = None
        self.child = set()
        self.spouse = set()

    @property
    def age(self):
        if self.birthday is None:
            return "NA"
            
        if self.death is not None:
            end_date = self.death
        else:
            end_date = datetime.today().date()
            
        calculated_age = end_date.year - self.birthday.year
        
        # Subtract 1 year if the current date is before their birthday in the current year
        if (end_date.month, end_date.day) < (self.birthday.month, self.birthday.day):
            calculated_age = calculated_age - 1
            
        return calculated_age

    @property
    def alive(self):
        return self.death is None

    def get_pt_row(self):
        if self.birthday is not None:
            bday_str = self.birthday.strftime("%Y-%m-%d")
        else:
            bday_str = "NA"
            
        if self.death is not None:
            death_str = self.death.strftime("%Y-%m-%d")
        else:
            death_str = "NA"
            
        if len(self.child) > 0:
            child_str = self.child
        else:
            child_str = "NA"
            
        if len(self.spouse) > 0:
            spouse_str = self.spouse
        else:
            spouse_str = "NA"
            
        return [self.id, self.name, self.gender, bday_str, self.age, self.alive, death_str, child_str, spouse_str]

class Family:
    def __init__(self, fam_id):
        self.id = fam_id
        self.married = None
        self.divorced = None
        self.husband_id = "NA"
        self.husband_name = "NA"
        self.wife_id = "NA"
        self.wife_name = "NA"
        self.children = set()

    def get_pt_row(self):
        if self.married is not None:
            marr_str = self.married.strftime("%Y-%m-%d")
        else:
            marr_str = "NA"
            
        if self.divorced is not None:
            div_str = self.divorced.strftime("%Y-%m-%d")
        else:
            div_str = "NA"
            
        if len(self.children) > 0:
            children_str = self.children
        else:
            children_str = "NA"
            
        return [self.id, marr_str, div_str, self.husband_id, self.husband_name, self.wife_id, self.wife_name, children_str]
