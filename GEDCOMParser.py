# Shadman Choudhury, Nadia Lara, Derrick Sual - Project 3 - GEDCOM Parsing Group Project

import os
from prettytable import PrettyTable
from models import *


class Tag:
    def __init__(self, line, parent):
        self.parent = parent
        self.line = line.rstrip()
        components = line.split()
        if len(components) == 0:
            return  # skip empty lines
        arguments = ""
        tag = ""
        level = int(components[0])
        valid = None

        if len(components) > 2:
            if components[2] in [
                "INDI",
                "FAM",
            ]:  # specific case with INDI and FAM, the tags are arg 2
                tag = components[2]
                arguments = components[1]
                valid = (
                    level == 0 and parent == None
                )  # valid location and argument, true if level is 0 and parent is None
                if len(components) > 3:  # too many arguments, invalid
                    arguments += " ".join(components[3:])
                    valid = False
            elif (
                components[1] == "INDI" or components[1] == "FAM"
            ):  # right tag, wrong arg for edge cases
                tag = components[1]
                arguments = " ".join(components[2:])
                valid = False
            else:
                tag = components[1]
                arguments = " ".join(components[2:])
        else:
            tag = components[1]
            arguments = " ".join(components[2:])

        self.level = level
        self.tag = tag
        self.arguments = arguments
        self.validFlag = ""
        if valid == None:
            self._validate()
        else:
            self.valid = valid
            if self.valid:
                self.validFlag = "Y"
            else:
                self.validFlag = "N"

    def _validate(self):
        components = self.arguments.split()
        if len(components) > 0:
            if (
                self.tag == "NOTE"
            ):  # any string works, valid if the level/parent is correct
                self.valid = self.level == 0 and self.parent == None
            elif (
                self.tag == "NAME"
            ):  # any string works, valid if level is 1, may not have surname, must be part of INDI
                self.valid = (
                    self.level == 1 and self.parent and self.parent.tag == "INDI"
                )
            else:  # Name, Note, Indi, Fam taken care of
                if self.tag == "DATE":
                    if (
                        self.parent
                        and self.parent.tag not in ["BIRT", "DEAT", "DIV", "MARR"]
                        or self.level != 2
                    ):
                        self.valid = False  # wrong parent or wrong level
                    else:
                        if (
                            len(components) == 3
                            and 0 < int(components[0]) < 32
                            and components[1]
                            in [
                                "JAN",
                                "FEB",
                                "MAR",
                                "APR",
                                "MAY",
                                "JUN",
                                "JUL",
                                "AUG",
                                "SEP",
                                "OCT",
                                "NOV",
                                "DEC",
                            ]
                            and 999 < int(components[2]) < 10000
                        ):
                            self.valid = True  # exact number of args for DATE, with the correct formatting
                        else:
                            self.valid = False
                elif self.tag in ["FAMC", "FAMS"]:
                    if (
                        self.parent
                        and self.parent.tag == "INDI"
                        and len(components) == 1
                    ):  # prereqs
                        self.valid = self.level == 1  # valid if level is 1
                    else:
                        self.valid = False  # too many args/wrong parent
                elif self.tag == "SEX":
                    if (
                        self.parent
                        and self.parent.tag == "INDI"
                        and len(components) == 1
                    ):
                        self.valid = self.level == 1 and components[0] in [
                            "M",
                            "F",
                        ]  # valid if correct level and specific argument
                    else:
                        self.valid = False  # too many arguments or wrong parent
                elif self.tag in ["HUSB", "WIFE", "CHIL"]:
                    if (
                        self.parent
                        and self.parent.tag == "FAM"
                        and len(components) == 1
                    ):
                        self.valid = self.level == 1  # valid if level is 1
                    else:
                        self.valid = (
                            False  # too many args, wrong parent, or wrong level
                        )
                else:
                    self.valid = False  # something went wrong, or not a valid tag
        else:
            if self.tag in ["HEAD", "TRLR"] and self.parent == None and self.level == 0:
                self.valid = True  # no parent for these cases and level is correct
            elif (
                self.tag in ["DIV", "MARR"]
                and self.parent
                and self.parent.tag == "FAM"
                and self.level == 1
            ):
                self.valid = True  # parent is correct and level is correct
            elif (
                self.tag in ["DEAT", "BIRT"]
                and self.parent
                and self.parent.tag == "INDI"
                and self.level == 1
            ):
                self.valid = True  # parent is correct and level is correct
            else:
                self.valid = False  # something went wrong, either parent or level is wrong or the tag needed more args

        if self.valid:
            self.validFlag = "Y"
        else:
            self.validFlag = "N"

    def print(self):  # print lines
        print(f"--> {self.line}")
        print(f"<-- {self.level}|{self.tag}|{self.validFlag}|{self.arguments}")


class GEDCOMParser:
    def __init__(self, file):
        tags = []
        levelIndexes = [-1, -1, -1]
        index = 0
        for l in file:
            node = Tag(l, None)
            if node.level == 0:
                levelIndexes = [index, -1, -1]
            elif node.level == 1:
                node.parent = tags[levelIndexes[0]]
                node._validate()
                levelIndexes[1] = index
                levelIndexes[2] = -1
            elif node.level == 2:
                node.parent = tags[levelIndexes[1]]
                node._validate()
                levelIndexes[2] = index
            tags.append(node)
            index += 1
        self.tags = tags
        return

    def extract_entities(self):
        self.individuals = {}
        self.families = {}

        current_entity = None
        last_date_tag = None

        for tag in self.tags:
            if not tag.valid:
                continue

            if tag.level == 0:
                if tag.tag == "INDI":
                    # Checks if the Individual ID is unique
                    if tag.arguments in self.individuals:
                        print(f"Error: Duplicate Individual ID {tag.arguments}")
                        continue
                    current_entity = Individual(tag.arguments)
                    self.individuals[tag.arguments] = current_entity
                elif tag.tag == "FAM":
                    current_entity = Family(tag.arguments)
                    self.families[tag.arguments] = current_entity
                else:
                    current_entity = None
            elif tag.level == 1 and current_entity:
                if isinstance(current_entity, Individual):
                    if tag.tag == "NAME":
                        current_entity.name = tag.arguments
                    elif tag.tag == "SEX":
                        current_entity.gender = tag.arguments
                    elif tag.tag == "FAMS":
                        current_entity.spouse.add(tag.arguments)
                    elif tag.tag == "FAMC":
                        current_entity.child.add(tag.arguments)
                    elif tag.tag in ["BIRT", "DEAT"]:
                        last_date_tag = tag.tag
                elif isinstance(current_entity, Family):
                    if tag.tag == "HUSB":
                        current_entity.husband_id = tag.arguments
                    elif tag.tag == "WIFE":
                        current_entity.wife_id = tag.arguments
                    elif tag.tag == "CHIL":
                        current_entity.children.add(tag.arguments)
                    elif tag.tag in ["MARR", "DIV"]:
                        last_date_tag = tag.tag
            elif tag.level == 2 and current_entity and tag.tag == "DATE":
                date_obj = parse_date(tag.arguments)
                if isinstance(current_entity, Individual):
                    if last_date_tag == "BIRT":
                        current_entity.birthday = date_obj
                    elif last_date_tag == "DEAT":
                        current_entity.death = date_obj
                elif isinstance(current_entity, Family):
                    if last_date_tag == "MARR":
                        current_entity.married = date_obj
                    elif last_date_tag == "DIV":
                        current_entity.divorced = date_obj

        # Second pass to populate Family names from Individuals
        for fam in self.families.values():
            if fam.husband_id in self.individuals:
                fam.husband_name = self.individuals[fam.husband_id].name
            if fam.wife_id in self.individuals:
                fam.wife_name = self.individuals[fam.wife_id].name

    def CheckBirthsBeforeDeaths(self):
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            if not validBirthAndDeath(indiv.birthday, indiv.death):
                if self.errorStr == "":
                    self.errorStr += (
                        "\n"  # add in the first \n if and only if we find errors
                    )
                # failed birth before death
                if indiv.death is not None and indiv.birthday is not None:
                    self.errorStr += (
                        "ERROR: INDIVIDUAL: US09: "
                        + str(indiv.id)
                        + ": Died "
                        + str(indiv.death)
                        + " before born "
                        + str(indiv.birthday)
                        + "\n"
                    )
                elif indiv.birthday is None:
                    self.errorStr += (
                        "ERROR: INDIVIDUAL: US09: "
                        + str(indiv.id)
                        + ": Missing Birthday\n"
                    )
        # return errorStr

    def CheckMarriedBeforeDeaths(self):
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            if(indiv.alive):
                continue
            #only people who died will get here
            #check the families, error if death happens before marriage
            for fam_id in indiv.spouse:
                fam = self.families[fam_id]
                if(fam.married > indiv.death):
                    if self.errorStr == "":
                        self.errorStr += (
                            "\n"  # add in the first \n if and only if we find errors
                        )
                    self.errorStr += (
                        "ERROR: INDIVIDUAL: US10: "
                        + str(indiv.id)
                        + " died on "
                        + str(indiv.death)
                        + " before marriage on "
                        + str(fam.married)
                        + " in family "
                        + str(fam.id)
                        + "\n"
                    )

    def CheckImpossibleAges(self):
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            if indiv.age == "N/A":
                continue
            if int(indiv.age) > 150:
                if self.errorStr == "":
                    self.errorStr += (
                        "\n"  # add in the first \n if and only if we find errors
                    )
                self.errorStr += (
                    "ERROR: INDIVIDUAL: US22: "
                    + str(indiv.id)
                    + ": Too Old, Aged "
                    + str(indiv.age)
                    + "\n"
                )
        # return errorStr

    def CheckSiblingSpacing(self):
        for fam_id in sorted(self.families.keys()):
            family = self.families[fam_id]
            children = list(family.children)

            for child in children:
                if child not in self.individuals:
                    continue

                if self.individuals[child].birthday is None:
                    continue

                child_birth = self.individuals[child].birthday

                for sibling in children:
                    if sibling == child or sibling not in self.individuals:
                        continue
                    if self.individuals[sibling].birthday is None:
                        continue

                    sibling_birth = self.individuals[sibling].birthday

                    if child_birth and sibling_birth:
                        months_diff = abs(
                            round((child_birth - sibling_birth).days / 30.4375)
                        )
                        if months_diff < 8:
                            if self.errorStr == "":
                                self.errorStr += "\n"  # add in the first \n if and only if we find errors
                            self.errorStr += (
                                "ERROR: FAMILY: US13: "
                                + str(fam_id)
                                + ": Siblings "
                                + str(child)
                                + " and "
                                + str(sibling)
                                + " have invalid spacing of "
                                + str(months_diff)
                                + " months\n"
                            )

    def print(self, output_filepath=None):
        self.extract_entities()

        output_str = ""
        output_str += "Individuals\n"
        pt_indi = PrettyTable()
        pt_indi.field_names = [
            "ID",
            "Name",
            "Gender",
            "Birthday",
            "Age",
            "Alive",
            "Death",
            "Child",
            "Spouse",
        ]
        for indi_id in sorted(self.individuals.keys()):
            pt_indi.add_row(self.individuals[indi_id].get_pt_row())
        output_str += str(pt_indi) + "\n"

        output_str += "\nFamilies\n"
        pt_fam = PrettyTable()
        pt_fam.field_names = [
            "ID",
            "Married",
            "Divorced",
            "Husband ID",
            "Husband Name",
            "Wife ID",
            "Wife Name",
            "Children",
        ]
        for fam_id in sorted(self.families.keys()):
            pt_fam.add_row(self.families[fam_id].get_pt_row())
        output_str += str(pt_fam) + "\n"

        # Error Checking printouts
        self.errorStr = ""
        self.CheckBirthsBeforeDeaths()
        self.CheckMarriedBeforeDeaths()
        self.CheckImpossibleAges()
        self.CheckSiblingSpacing()
        output_str += self.errorStr

        # Print to console
        print(output_str)

        # Write to file
        if output_filepath is not None:
            try:
                with open(output_filepath, "w") as out_file:
                    out_file.write(output_str)
                print(f"Output successfully written to {output_filepath}\n")
            except Exception as e:
                print(f"Error writing to output file: {e}\n")


def main():
    filename = ""
    loop = True
    while loop == True:
        filename = input("Please Enter Filename: ")
        try:
            file = open(filename, "r")
            loop = False
        except FileNotFoundError:
            print("Error: File does not exist. Please try again.")
        except PermissionError:
            print("Error: File could not be read. Please try again.")
        except:
            print("Unknown Error, please try again.")

    base, _ = os.path.splitext(filename)
    output_filename = base + "_output.txt"

    parser = GEDCOMParser(file)
    parser.print(output_filename)


if __name__ == "__main__":
    main()
