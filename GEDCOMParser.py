# Shadman Choudhury, Nadia Lara, Derrick Sual - Project 3 - GEDCOM Parsing Group Project

import os
from prettytable import PrettyTable
from models import *


class Tag:
    def __init__(self, line, parent, line_num=None):
        self.parent = parent
        self.line_num = line_num
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
        for line_num, l in enumerate(file, 1):
            node = Tag(l, None, line_num=line_num)
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
        self.errorStr = ""
        return

    def _add_error(self, message, line_num=None):
        """Append an error message to errorStr, adding a leading newline before the first error."""
        if self.errorStr == "":
            self.errorStr += "\n"
        if line_num is not None:
            self.errorStr += f"Line {line_num}: {message}\n"
        else:
            self.errorStr += message + "\n"

    def _process_individual_tag(self, individual, tag):
        """Handle level-1 tags for an Individual entity. Returns the date tag name if applicable."""
        if tag.tag == "NAME":
            individual.name = tag.arguments
        elif tag.tag == "SEX":
            individual.gender = tag.arguments
        elif tag.tag == "FAMS":
            individual.spouse.add(tag.arguments)
        elif tag.tag == "FAMC":
            individual.child.add(tag.arguments)
        elif tag.tag in ["BIRT", "DEAT"]:
            return tag.tag
        return None

    def _process_family_tag(self, family, tag):
        """Handle level-1 tags for a Family entity. Returns the date tag name if applicable."""
        if tag.tag == "HUSB":
            family.husband_id = tag.arguments
        elif tag.tag == "WIFE":
            family.wife_id = tag.arguments
        elif tag.tag == "CHIL":
            family.children.add(tag.arguments)
        elif tag.tag in ["MARR", "DIV"]:
            return tag.tag
        return None

    def _apply_date(self, entity, last_date_tag, date_obj):
        """Apply a parsed date to the correct field on an Individual or Family."""
        if isinstance(entity, Individual):
            if last_date_tag == "BIRT":
                entity.birthday = date_obj
            elif last_date_tag == "DEAT":
                entity.death = date_obj
        elif isinstance(entity, Family):
            if last_date_tag == "MARR":
                entity.married = date_obj
            elif last_date_tag == "DIV":
                entity.divorced = date_obj

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
                    current_entity = Individual(tag.arguments, line_num=tag.line_num)
                    self.individuals[tag.arguments] = current_entity
                elif tag.tag == "FAM":
                    current_entity = Family(tag.arguments, line_num=tag.line_num)
                    self.families[tag.arguments] = current_entity
                else:
                    current_entity = None
            elif tag.level == 1 and current_entity:
                if isinstance(current_entity, Individual):
                    date_tag = self._process_individual_tag(current_entity, tag)
                elif isinstance(current_entity, Family):
                    date_tag = self._process_family_tag(current_entity, tag)
                else:
                    date_tag = None
                if date_tag is not None:
                    last_date_tag = date_tag
            elif tag.level == 2 and current_entity and tag.tag == "DATE":
                self._apply_date(
                    current_entity, last_date_tag, parse_date(tag.arguments)
                )

        # Second pass to populate Family names from Individuals
        for fam in self.families.values():
            if fam.husband_id in self.individuals:
                fam.husband_name = self.individuals[fam.husband_id].name
            if fam.wife_id in self.individuals:
                fam.wife_name = self.individuals[fam.wife_id].name

    def checkUniqueIDs(self):
        ids = set()
        for tag in self.tags:
            # ensuring it is valid, assigned a level of 0 and has the correct tag
            if tag.valid and tag.level == 0 and tag.tag == "INDI":
                # will add the value to the ids otherwise if a duplicate is detected it will add an error
                if tag.arguments in ids:
                    self._add_error(
                        "ERROR: INDIVIDUAL: US04: "
                        + str(tag.arguments)
                        + ": Duplicated Individual ",
                        line_num=tag.line_num,
                    )
                else:
                    ids.add(tag.arguments)

    def CheckBirthsBeforeDeaths(self):
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            # Must check "N/A" first to avoid Python 3 TypeError (comparing str and int).
            # Living people with future birthdays have negative age but are caught in CheckPossibleDates.
            if indiv.age == "N/A" or indiv.age < 0:
                # failed birth before death
                if indiv.death is not None and indiv.birthday is not None:
                    self._add_error(
                        "ERROR: INDIVIDUAL: US09: "
                        + str(indiv.id)
                        + ": Died "
                        + str(indiv.death)
                        + " before born "
                        + str(indiv.birthday),
                        line_num=indiv.line_num,
                    )
                elif indiv.birthday is None:
                    self._add_error(
                        "ERROR: INDIVIDUAL: US09: "
                        + str(indiv.id)
                        + ": Missing Birthday",
                        line_num=indiv.line_num,
                    )
        # return errorStr

    def CheckMarriedBeforeDeaths(self):
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            if indiv.alive:
                continue
            # only people who died will get here
            # check the families, error if death happens before marriage
            for fam_id in indiv.spouse:
                fam = self.families[fam_id]
                if (
                    fam.married is not None and fam.married > indiv.death
                ):  # catches edge case where marriage date was not saved
                    self._add_error(
                        "ERROR: INDIVIDUAL: US10: "
                        + str(indiv.id)
                        + " died on "
                        + str(indiv.death)
                        + " before marriage on "
                        + str(fam.married)
                        + " in family "
                        + str(fam.id),
                        line_num=indiv.line_num,
                    )

    def CheckBigamy(self):
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            fams = {}  # will hold the family data for each individual
            # check the families for each individual
            # error if marriage happens before divorce or spouse death
            for fam_id in indiv.spouse:
                fam = self.families[fam_id]
                husb_id = fam.husband_id
                wife_id = fam.wife_id
                # for each family, the relevant data is spouse (for potential death date), marriage date, divorce date
                if indiv_id == husb_id:
                    fams[fam_id] = (wife_id, fam.married, fam.divorced)
                else:
                    fams[fam_id] = (husb_id, fam.married, fam.divorced)
                if (
                    fam.married is None
                ):  # catches edge case where marriage date was not saved
                    self._add_error(
                        "ERROR: INDIVIDUAL: US12: "
                        + str(husb_id)
                        + " married to "
                        + str(wife_id)
                        + " from family "
                        + str(fam.id)
                        + " has no marriage date",
                        line_num=fam.line_num,
                    )
            # we have highlighted all families without marriage dates at this point
            # now we have the families the individual was part of, time to check them against each other
            for fam_id in sorted(fams.keys()):
                fam = fams[fam_id]
                firstSpouse = self.individuals[fam[0]]
                firstEndDate = None
                firstCurrentMarriage = True
                if (
                    fam[2] == None and firstSpouse.alive
                ):  # no divorce date set, spouse is alive, active marriage
                    firstCurrentMarriage = True
                elif fam[2] == None:  # no divorce, but spouse has passed
                    firstCurrentMarriage = False
                    firstEndDate = firstSpouse.death
                elif firstSpouse.alive:  # divorce, living spouse
                    firstCurrentMarriage = False
                    firstEndDate = fam[2]
                else:  # divorce and the spouse passed, we go with whichever happened first
                    # ideally this is the divorce date, but this should catch edge cases as well
                    firstCurrentMarriage = False
                    firstEndDate = min(fam[2], firstSpouse.death)

                # we have the base marriage we are comparing against, now to check each family against it
                for other_fam_id in sorted(fams.keys()):
                    if fam_id == other_fam_id:
                        continue  # skip comparing to same family
                    other_fam = fams[other_fam_id]
                    secondSpouse = self.individuals[other_fam[0]]
                    secondEndDate = None
                    secondCurrentMarriage = True
                    if (
                        other_fam[2] == None and secondSpouse.alive
                    ):  # no divorce date set, spouse is alive, active marriage
                        secondCurrentMarriage = True
                    elif other_fam[2] == None:  # no divorce, but spouse has passed
                        secondCurrentMarriage = False
                        secondEndDate = secondSpouse.death
                    elif secondSpouse.alive:  # divorce, living spouse
                        secondCurrentMarriage = False
                        secondEndDate = other_fam[2]
                    else:  # divorce and the spouse passed, we go with whichever happened first
                        # ideally this is the divorce date, but this should catch edge cases as well
                        secondCurrentMarriage = False
                        secondEndDate = min(other_fam[2], secondSpouse.death)
                    # now we have the data for both families
                    if (
                        firstCurrentMarriage and secondCurrentMarriage
                    ):  # explicit current bigamy, both active marriages
                        self._add_error(
                            "ERROR: FAMILY: US12: "
                            + str(fam_id)
                            + " is a current marriage starting "
                            + str(fam[1])
                            + " and "
                            + str(other_fam_id)
                            + " is also a current marriage starting "
                            + str(other_fam[1]),
                            line_num=(
                                self.families[fam_id].line_num
                                if fam_id in self.families
                                else None
                            ),
                        )
                    elif (
                        firstCurrentMarriage
                        and fam[1] != None
                        and fam[1] < secondEndDate
                    ):  # First marriage active, second marriage ended after first one started
                        self._add_error(
                            "ERROR: FAMILY: US12: "
                            + str(fam_id)
                            + " married on "
                            + str(fam[1])
                            + " but "
                            + str(other_fam_id)
                            + " ended on "
                            + str(secondEndDate),
                            line_num=(
                                self.families[fam_id].line_num
                                if fam_id in self.families
                                else None
                            ),
                        )
                    elif (
                        secondCurrentMarriage
                        and other_fam[1] != None
                        and other_fam[1] < firstEndDate
                    ):  # second marriage started before first marriage ended
                        self._add_error(
                            "ERROR: FAMILY: US12: "
                            + str(other_fam_id)
                            + " married on "
                            + str(other_fam[1])
                            + " but "
                            + str(fam_id)
                            + " ended on "
                            + str(firstEndDate),
                            line_num=(
                                self.families[other_fam_id].line_num
                                if other_fam_id in self.families
                                else None
                            ),
                        )
                    elif (
                        fam[1] != None
                        and other_fam[1] != None
                        and secondEndDate is not None
                        and fam[1] < secondEndDate
                        and secondEndDate < firstEndDate
                    ):  # both marriages have ended, one started before the other ended
                        self._add_error(
                            "ERROR: FAMILY: US12: "
                            + str(fam_id)
                            + " married on "
                            + str(fam[1])
                            + " and ended on "
                            + str(firstEndDate)
                            + " but "
                            + str(other_fam_id)
                            + " married on "
                            + str(other_fam[1])
                            + " and ended on "
                            + str(secondEndDate),
                            line_num=(
                                self.families[fam_id].line_num
                                if fam_id in self.families
                                else None
                            ),
                        )

    def CheckImpossibleAges(self):
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            if indiv.birthday == None:
                continue
            if int(indiv.age) > 150:
                self._add_error(
                    "ERROR: INDIVIDUAL: US22: "
                    + str(indiv.id)
                    + ": Too Old, Aged "
                    + str(indiv.age),
                    line_num=indiv.line_num,
                )
        # return errorStr

    def CheckSiblingSpacing(self):
        approx_days_in_month = 30.4375
        twins_threshold_days = 2
        general_sibling_threshold_months = 8

        for fam_id in sorted(self.families.keys()):
            family = self.families[fam_id]
            # Filter children who exist and have a valid birthdate
            valid_children = []
            for child_id in family.children:
                if child_id in self.individuals:
                    if self.individuals[child_id].birthday is not None:
                        valid_children.append(child_id)

            valid_children.sort()

            # Compare unique pairs of siblings
            for i in range(len(valid_children)):
                for j in range(i + 1, len(valid_children)):
                    child1 = valid_children[i]
                    child2 = valid_children[j]

                    birth1 = self.individuals[child1].birthday
                    birth2 = self.individuals[child2].birthday

                    days_diff = abs((birth1 - birth2).days)
                    months_diff = abs(round(days_diff / approx_days_in_month))

                    # Comparing between days and months
                    if (
                        days_diff >= twins_threshold_days
                        and months_diff < general_sibling_threshold_months
                    ):
                        self._add_error(
                            f"ERROR: FAMILY: US13: {fam_id}: Siblings {child1} and {child2} have invalid spacing of {months_diff} months",
                            line_num=family.line_num,
                        )

    def CheckCorrectGenderForRole(self):
        for fam in self.families.values():
            husband = self.individuals.get(fam.husband_id)
            wife = self.individuals.get(fam.wife_id)
            # Checks to make sure husband is assigned M and wife is assigned F
            if husband and husband.gender != "M":
                self._add_error(
                    "ERROR: FAMILY: US07: "
                    + str(fam.id)
                    + ": Husband "
                    + str(husband.id)
                    + " has invalid sex. Female when should be male.",
                    line_num=fam.line_num,
                )
            if wife and wife.gender != "F":
                self._add_error(
                    "ERROR: FAMILY: US07: "
                    + str(fam.id)
                    + ": Wife "
                    + str(wife.id)
                    + " has invalid sex. Male when should be female.",
                    line_num=fam.line_num,
                )

    def CheckMarriageToDescendants(self):
        for fam_id in sorted(self.families.keys()):
            fam = self.families[fam_id]
            husband = self.individuals.get(fam.husband_id)
            wife = self.individuals.get(fam.wife_id)

            if not husband or not wife:
                continue

            if self.is_descendant(husband.id, wife.id):
                self._add_error(
                    f"ERROR: FAMILY: US15: {fam.id}: Husband {husband.id} is a descendant of Wife {wife.id}.",
                    line_num=fam.line_num,
                )

            if self.is_descendant(wife.id, husband.id):
                self._add_error(
                    f"ERROR: FAMILY: US15: {fam.id}: Wife {wife.id} is a descendant of Husband {husband.id}.",
                    line_num=fam.line_num,
                )

    def checkSiblingMarriage(self):
        for fam_id in sorted(self.families.keys()):
            fam = self.families[fam_id]
            husb_id = fam.husband_id
            wife_id = fam.wife_id
            if wife_id == husb_id:
                self._add_error(
                    "ERROR: FAMILY: US16: "
                    + str(fam_id)
                    + ": has both husband and wife as "
                    + str(husb_id),
                    line_num=fam.line_num,
                )
            elif self.is_sibling(husb_id, wife_id):
                self._add_error(
                    "ERROR: FAMILY: US16: "
                    + str(fam_id)
                    + ": Husband "
                    + str(husb_id)
                    + " is sibling of Wife "
                    + str(wife_id),
                    line_num=fam.line_num,
                )

    def checkAuntUncleMarriage(self):
        # Note: This check relies on is_sibling, which only returns True for full siblings (sharing a common child family ID) and does not cover half-siblings.
        # Note: This check only validates direct aunt/uncle and niece/nephew relationships; it does not check grand-aunt/grand-uncle relationships.
        for fam_id in sorted(self.families.keys()):
            fam = self.families[fam_id]
            husb_id = fam.husband_id
            wife_id = fam.wife_id

            husband = self.individuals.get(husb_id)
            wife = self.individuals.get(wife_id)
            if not husband or not wife:
                continue

            # Check if husband is an uncle of wife (husband is sibling of a parent of wife)
            for parent_fam_id in wife.child:
                if parent_fam_id in self.families:
                    parent_fam = self.families[parent_fam_id]
                    for parent_id in [parent_fam.husband_id, parent_fam.wife_id]:
                        if parent_id in self.individuals and self.is_sibling(
                            husb_id, parent_id
                        ):
                            if husb_id != parent_id:
                                self._add_error(
                                    f"ERROR: FAMILY: US17: {fam_id}: Husband {husb_id} is uncle of Wife {wife_id}.",
                                    line_num=fam.line_num,
                                )
                                break
                    else:
                        continue
                    break

            # Check if wife is an aunt of husband (wife is sibling of a parent of husband)
            for parent_fam_id in husband.child:
                if parent_fam_id in self.families:
                    parent_fam = self.families[parent_fam_id]
                    for parent_id in [parent_fam.husband_id, parent_fam.wife_id]:
                        if parent_id in self.individuals and self.is_sibling(
                            wife_id, parent_id
                        ):
                            if wife_id != parent_id:
                                self._add_error(
                                    f"ERROR: FAMILY: US17: {fam_id}: Wife {wife_id} is aunt of Husband {husb_id}.",
                                    line_num=fam.line_num,
                                )
                                break
                    else:
                        continue
                    break

    def checkCousinMarriage(self):
        # Note: This check relies on is_sibling, which only returns True for full siblings (sharing a common child family ID) and does not cover half-siblings.
        # Note: This check only validates first cousin relationships.
        for fam_id in sorted(self.families.keys()):
            fam = self.families[fam_id]
            husb_id = fam.husband_id
            wife_id = fam.wife_id

            husband = self.individuals.get(husb_id)
            wife = self.individuals.get(wife_id)
            if not husband or not wife:
                continue

            if self.is_sibling(husb_id, wife_id):
                continue

            husb_parents = []
            for parent_fam_id in husband.child:
                if parent_fam_id in self.families:
                    parent_fam = self.families[parent_fam_id]
                    for p_id in [parent_fam.husband_id, parent_fam.wife_id]:
                        if p_id in self.individuals:
                            husb_parents.append(p_id)

            wife_parents = []
            for parent_fam_id in wife.child:
                if parent_fam_id in self.families:
                    parent_fam = self.families[parent_fam_id]
                    for p_id in [parent_fam.husband_id, parent_fam.wife_id]:
                        if p_id in self.individuals:
                            wife_parents.append(p_id)

            if husb_id in wife_parents or wife_id in husb_parents:
                continue

            is_uncle = False
            for wp_id in wife_parents:
                if self.is_sibling(husb_id, wp_id) and husb_id != wp_id:
                    is_uncle = True
                    break
            if is_uncle:
                continue

            is_aunt = False
            for hp_id in husb_parents:
                if self.is_sibling(wife_id, hp_id) and wife_id != hp_id:
                    is_aunt = True
                    break
            if is_aunt:
                continue

            is_cousin = False
            for hp_id in husb_parents:
                for wp_id in wife_parents:
                    if hp_id != wp_id and self.is_sibling(hp_id, wp_id):
                        is_cousin = True
                        break
                if is_cousin:
                    break

            if is_cousin:
                self._add_error(
                    f"ERROR: FAMILY: US18: {fam_id}: Husband {husb_id} and Wife {wife_id} are first cousins.",
                    line_num=fam.line_num,
                )

    def is_sibling(self, person1_id, person2_id):
        # Note: This check only returns True for full siblings (sharing a common child family ID) and does not cover half-siblings.
        if person1_id == person2_id:  # you are definitely related to yourself
            return True
        person1 = self.individuals[person1_id]
        person2 = self.individuals[person2_id]
        for fam_id in person1.child:
            if (
                fam_id in person2.child
            ):  # they share a family where they are both children
                return True
        return False

    def is_descendant(self, descendant_id, ancestor_id, visited=None):
        if descendant_id == ancestor_id:
            return True

        if visited is None:
            visited = set()
        if descendant_id in visited:
            return False
        visited.add(descendant_id)

        if descendant_id not in self.individuals:
            return False

        individual = self.individuals[descendant_id]
        for fam_id in individual.child:
            if fam_id in self.families:
                family = self.families[fam_id]
                for parent in [family.husband_id, family.wife_id]:
                    if self.is_descendant(parent, ancestor_id, visited):
                        return True
        return False

    def CheckPossibleDates(self):
        end_date = datetime.today().date()
        # comparing the current date with the birthday and death date for each individual to ensure the birth and death dates are valid
        for indiv in self.individuals.values():
            if indiv.birthday and end_date < indiv.birthday:
                self._add_error(
                    "ERROR: INDIVIDUAL: US08: "
                    + str(indiv.id)
                    + ": Birthday "
                    + str(indiv.birthday)
                    + " is after current date "
                    + str(end_date),
                    line_num=indiv.line_num,
                )
            if indiv.death and end_date < indiv.death:
                self._add_error(
                    "ERROR: INDIVIDUAL: US08: "
                    + str(indiv.id)
                    + ": Death date "
                    + str(indiv.death)
                    + " is after current date "
                    + str(end_date),
                    line_num=indiv.line_num,
                )
            # for family roles, comparing the current date with individuals with marriage dates and divorced dates have valid dates
            for fam_id in indiv.spouse:
                fam = self.families[fam_id]
                if fam.married and end_date < fam.married:
                    self._add_error(
                        "ERROR: FAMILY: US08: "
                        + str(indiv.id)
                        + ": Married date "
                        + str(fam.married)
                        + " is after current date "
                        + str(end_date),
                        line_num=indiv.line_num,
                    )
                if fam.divorced and end_date < fam.divorced:
                    self._add_error(
                        "ERROR: FAMILY: US08: "
                        + str(indiv.id)
                        + ": Divorced date "
                        + str(fam.divorced)
                        + " is after current date "
                        + str(end_date),
                        line_num=indiv.line_num,
                    )

    def MarriageAfterFourteen(self):
        # for fam in self.families.values():
        for indiv in self.individuals.values():
            for fam_id in indiv.spouse:
                fam = self.families[fam_id]
                if fam.married and indiv.birthday:
                    age = (fam.married - indiv.birthday).days / 365.25
                    if age < 14:
                        self._add_error(
                            "ERROR: INDIVIDUAL: US11: "
                            + str(indiv.id)
                            + ": Marriage age is under 14 "
                            + str(fam.married),
                            line_num=indiv.line_num,
                        )

    def LessThanFiveBirths(self):
        for fam in self.families.values():
            births = {}
            for child_id in fam.children:
                child = self.individuals.get(child_id)
                if child and child.birthday:
                    if child.birthday in births:
                        births[child.birthday].append(child_id)
                    else:
                        births[child.birthday] = [child_id]
            for birthday, siblings in births.items():
                if len(siblings) > 5:
                    self._add_error(
                        "ERROR: FAMILY: US14: "
                        + str(fam.id)
                        + ": More than 5 siblins born on "
                        + str(birthday)
                        + ": "
                        + ", ".join(siblings),
                        line_num=fam.line_num,
                    )

    def PrintRecentlyBorn(self):
        result = "\nRecently Born Individuals\n"
        pt_born = PrettyTable()
        pt_born.field_names = [
            "ID",
            "Name",
            "Gender",
            "Birthday",
        ]
        foundCount = 0
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            lastYear = datetime.today() - timedelta(days=365)
            if indiv.birthday == None:
                # no listed birthday, don't want to add to list
                continue
            if indiv.birthday >= lastYear.date():
                rowList = [indiv.id, indiv.name, indiv.gender, indiv.birthday]
                pt_born.add_row(rowList)
                foundCount += 1
        if foundCount == 0:
            result += "None Found\n"
        else:
            result += str(pt_born) + "\n"
        return result

    def PrintLivingMarried(self):
        result = "\nLiving Married Individuals\n"
        pt_married = PrettyTable()
        pt_married.field_names = [
            "ID",
            "Name",
            "Gender",
            "Spouse ID",
        ]
        foundCount = 0
        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            if indiv.death != None and indiv.death <= datetime.today().date():
                # died and not will die in the future (weird edge case,
                # but possible in cases of cancer, etc where a death is planned)
                # don't want to add to list
                continue
            spouses = indiv.spouse
            if len(spouses) > 0:
                rowList = [indiv.id, indiv.name, indiv.gender]
                spousesList = []
                for fam_id in sorted(spouses):
                    # explicitly and intentionally allows multiple current marriages per person
                    # because bigamy is bad but technically possible in the real world
                    fam = self.families[fam_id]
                    if fam.divorced != None and fam.divorced <= datetime.today().date():
                        # family is divorced already, excludes future divorce dates, which
                        # can be planned but are still legally valid marriages at the time
                        # don't want to add to list
                        continue
                    spouse_id = ""
                    if fam.husband_id == indiv_id:
                        spouse_id = fam.wife_id
                    else:
                        spouse_id = fam.husband_id
                    spouse = self.individuals[spouse_id]
                    if spouse.death != None and spouse.death <= datetime.today().date():
                        # same death case as regular individuals, don't want to add to list
                        continue
                    spousesList.append(spouse_id)
                if len(spousesList) > 0:
                    rowList.append(spousesList)
                    pt_married.add_row(rowList)
                    foundCount += 1
        if foundCount == 0:
            result += "None Found\n"
        else:
            result += str(pt_married) + "\n"
        return result

    def PrintDeceasedIndividuals(self):
        result = "\nDeceased Individuals\n"
        pt_deceased = PrettyTable()
        pt_deceased.field_names = [
            "ID",
            "Name",
            "Gender",
            "Death",
        ]
        foundCount = 0

        for indiv_id in sorted(self.individuals.keys()):
            indiv = self.individuals[indiv_id]
            if indiv.death is not None:
                rowList = [indiv.id, indiv.name, indiv.gender, indiv.death]
                pt_deceased.add_row(rowList)
                foundCount += 1

        if foundCount == 0:
            result += "None Found\n"
        else:
            result += str(pt_deceased) + "\n"
        return result

    def UniqueNameandBirth(self):
        pairs = {}
        for indiv in self.individuals.values():
            if indiv.name and indiv.birthday:
                list = (indiv.name, indiv.birthday)
                if list in pairs:
                    pairs[list].append(indiv.id)
                else:
                    pairs[list] = [indiv.id]
        for (name, birthday), matches in pairs.items():
            if len(matches) > 1:
                first_indiv_line = (
                    self.individuals[matches[0]].line_num
                    if matches[0] in self.individuals
                    else None
                )
                self._add_error(
                    "ERROR: INDIVIDUAL: US19: "
                    + ", ".join(matches)
                    + ": Same name ("
                    + str(name)
                    + ") and birth date ("
                    + str(birthday)
                    + ")",
                    line_num=first_indiv_line,
                )

    def RejectIllegitimateDates(self):
        days_month = {
            "JAN": 31,
            "FEB": 28,
            "MAR": 31,
            "APR": 30,
            "MAY": 31,
            "JUN": 30,
            "JUL": 31,
            "AUG": 31,
            "SEP": 30,
            "OCT": 31,
            "NOV": 30,
            "DEC": 31,
        }

        for tag in self.tags:
            if tag.tag == "DATE" and tag.valid:
                components = tag.arguments.split()
                if len(components) != 3:
                    continue
                day1, month1, yr1 = components
                day = int(day1)
                year = int(yr1)
                max_day = days_month[month1]

                # Handles the case of February in leap years
                if month1 == "FEB":
                    leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
                    if leap:
                        max_day = 29
                if day > max_day:
                    self._add_error(
                        "ERROR: DATE: US23: "
                        + str(day)
                        + " "
                        + month1
                        + " "
                        + str(year)
                        + " is not a legitimate date ("
                        + month1
                        + " only has "
                        + str(max_day)
                        + " days in "
                        + str(year)
                        + ")",
                        line_num=tag.line_num,
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

        output_str += self.PrintLivingMarried()

        output_str += self.PrintRecentlyBorn()

        output_str += self.PrintDeceasedIndividuals()

        # Error Checking printouts
        # self.errorStr = "" #gets set in the init to allow for ease of testing
        self.CheckBirthsBeforeDeaths()
        self.CheckMarriedBeforeDeaths()
        self.CheckImpossibleAges()
        self.CheckSiblingSpacing()
        self.CheckCorrectGenderForRole()
        self.CheckMarriageToDescendants()
        self.CheckPossibleDates()
        self.checkUniqueIDs()
        self.CheckBigamy()
        self.checkSiblingMarriage()
        self.checkAuntUncleMarriage()
        self.checkCousinMarriage()
        self.MarriageAfterFourteen()
        self.LessThanFiveBirths()
        self.UniqueNameandBirth()
        self.RejectIllegitimateDates()

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
