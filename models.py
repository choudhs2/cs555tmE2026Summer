from datetime import datetime, date
from typing import Optional, Set

def parse_date(date_str: str) -> Optional[date]:
    try:
        return datetime.strptime(date_str, "%d %b %Y").date()
    except ValueError:
        return None

class Individual:
    def __init__(self, indi_id: str):
        self.id: str = indi_id
        self.name: str = "NA"
        self.gender: str = "NA"
        self.birthday: Optional[date] = None
        self.death: Optional[date] = None
        self.child: Set[str] = set()
        self.spouse: Set[str] = set()

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
    def alive(self) -> bool:
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
    def __init__(self, fam_id: str):
        self.id: str = fam_id
        self.married: Optional[date] = None
        self.divorced: Optional[date] = None
        self.husband_id: str = "NA"
        self.husband_name: str = "NA"
        self.wife_id: str = "NA"
        self.wife_name: str = "NA"
        self.children: Set[str] = set()

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
