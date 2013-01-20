import sys
import subprocess
import csv
import argparse

import settings

def load_people(filename="people.csv"):
    r = csv.reader(open(filename))
    people = {}
    for person in r:
        people[person[0]] = [person[1], person[2]]
        if not person[1]:
            people[person[0]][0] = person[0].title()
    return people

def save_person(nick, desc, name=None, filename="people.csv"):
    with open(filename, 'ab') as csvfile:
        w = csv.writer(csvfile)
        w.writerow([nick, name, desc])

def handle_save(args):
    if args.nickname is not None:
        save_person(args.nickname, args.description, args.name)
    else:
        save_person(args.name, args.description)

def handle_intro(args):
     people = load_people()

     if len(args.people) < 2:
         sys.exit("At least two people are required to make an introduction.")

     introducing = {} # get the people data from the set
     for person in args.people:
         try:
             introducing[person] = people[person]
         except KeyError, e:
             print "Missing person %s in your data!" % e
             sys.exit()

     msg = write_introduction(introducing, args.message)
     print msg
     p = subprocess.Popen(["pbcopy"],stdin=subprocess.PIPE)
     p.stdin.write(msg)


def write_introduction(people, message):
    nicks, infos = zip(*(people.items()))
    names, descriptions = zip(*infos)

    i = ", ".join(names[:-1]) + " & " + names[-1] + ", please meet.\n\n"
    i += "\n\n".join(descriptions)
    if message:
        i += "\n\n" + message
    else:
        i += "\n\n" + settings.closing
    i += "\n\n" + settings.valediction + ",\n\n" + settings.name
    return i


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title="subcommand", help="subcommand help")
    add_parser = subparsers.add_parser('add', help="add a person")
    add_parser.add_argument(
        "nickname", help="the person's nickname, used by the `message` "
        "command to refer to this person (default: the person's name)",
        nargs='?')
    add_parser.add_argument("name", help="the person's name")
    add_parser.add_argument(
        "description", help="a description of this person, used to introduce "
        "them to other people")
    add_parser.set_defaults(func=handle_save)

    message_parser = subparsers.add_parser(
        "intro", help="introduce people to one another")
    message_parser.add_argument(
        "-m", "--message", default=False, action="store", help="a custom "
        "message introducing these people to one another")
    message_parser.add_argument(
        "people", nargs="+", help="the people being introduced "
        "to one another")
    message_parser.set_defaults(func=handle_intro)

    args = parser.parse_args()

    args.func(args)
