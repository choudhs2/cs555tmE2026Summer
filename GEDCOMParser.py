# Shadman Choudhury, Nadia Lara, Derrick Sual - Project 3 - GEDCOM Parsing Group Project


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

    def print(self):
        for i in self.tags:
            i.print()


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
    parser = GEDCOMParser(file)
    parser.print()


main()
