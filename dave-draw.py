#!/usr/bin/env python3
import pdb
import random
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Viewer(object):
    def __init__(self,
                 viewer_id,
                 twitch_name,
                 viewer_type,
                 points2,
                 hours,
                 last_seen,
                 sub
                 ):
        self.viewer_id = viewer_id
        self.twitch_name = twitch_name
        self.viewer_type = viewer_type
        self.points2 = points2
        self.hours = hours
        self.last_seen = last_seen
        self.sub = sub

    def win_chance(self, total_tickets):
        """
        Takes the total tickets (points) as a paramter and works
        out the percentage chance that the viewer has of winning.

        Returns the viewers win chance in percent.
        """

        percent = total_tickets / 100.00

        return self.points2 / percent


class DaveDraw(object):
    def __init__(self):
        self.debug = False
        self.database_path = 'Viewers3DB.sqlite'
        self.db_conn = sqlite3.connect(self.database_path)
        self.get_viewers()
        self.calculate_total_points()
        self.assign_tickets()

    def assign_tickets(self):
        """
        Assigns each user a number range based on the number of
        tickets they have.

        e.g.
        10 1-10
        10 11-20
        30 21-50
        1  51
        """

        self.tickets = {}
        latest_ticket = 0

        for viewer in self.viewers:
            # skip anyone with less than 500 points
            if viewer.points2 <= 500:
                continue

            ticket_range_beg = latest_ticket + 1
            ticket_range_end = latest_ticket + 1 + viewer.points2
            latest_ticket = ticket_range_end

            viewer.tickets = range(ticket_range_beg, ticket_range_end)

            # assign a range of tickets:
            if self.debug:
                print("Assigning viewer twitch: %s tickets %i-%i" % (viewer.twitch_name, viewer.tickets.start, viewer.tickets.stop))
            if ticket_range_beg == ticket_range_end:
                if self.debug:
                    print("Assigning ticket {} to {}".format(ticket_range_beg,
                          viewer.twitch_name))
                self.tickets[ticket_range_beg] = viewer
                next

            for ticket in viewer.tickets:
                if self.debug:
                    print("Assigning ticket {} to {}".format(ticket,
                          viewer.twitch_name))
                self.tickets[ticket] = viewer

    def calculate_total_points(self):
        """
        Gets the total amount of points awarded to all
        viewers.
        """

        self.total_points = 0
        for viewer in self.viewers:
            self.total_points += viewer.points2

        self.total_points_percent = self.total_points / 100

        print("Total points awarded (total tickets): %s" % self.total_points)

    def draw(self):
        """
        Picks a random number between 1 and total tickets, finds
        the user that has been assigned tickets within that range and
        returns the user.
        """

        ticket = random.randint(1, list(self.tickets.keys())[-1])

        try:
            winner = self.tickets[ticket]
        except:
            pdb.set_trace()

        print("\n===== WINNER {} =====\n".format(winner.twitch_name))
        print("Picked ticket {}\n".format(ticket))
        print("Winner win chance: {:f}".format(
            winner.win_chance(self.total_points)))
        print("Winner's ticket range: {}-{}".format(
            winner.tickets.start, winner.tickets.stop))
        print("Winner's ticket amount: {}\n".format(winner.points2))

        self.display_viewer(winner)

    def display_random_viewer(self):
        """
        Displays random viewer.
        """
        self.display_viewer(self.get_random_viewer())

    def display_viewer(self, viewer):
        """
        Outputs the data on all viewers.
        """
        print("""Twitch Name: %s\n\nPoints: %s\nHours: %s\nLastSeen: %s\n"""
              % (
                    viewer.twitch_name,
                    viewer.points2,
                    viewer.hours,
                    viewer.last_seen
                )
              )

    def get_random_viewer(self):
        """
        Gets a completely random viewer.
        """
        return random.choice(self.viewers)

    def get_viewers(self):
        """
        Gets data on all the viewers in the database and stores
        the data in self.viewers.
        """
        c = self.db_conn.cursor()
        c.row_factory = dict_factory

        c.execute('''
                SELECT

                v_id,
                TwitchName,
                Type,
                Points2,
                Hours,
                LastSeen,
                Sub

                FROM Viewer
                WHERE Type != 1
                AND TwitchName NOT IN (
                    \'treeboydave\',
                    \'treebotdave\',
                    \'stay_hydrated_bot\'
                );
                ''')

        self.viewers = []

        for cur_viewer in c:
            self.viewers.append(
                    Viewer(
                        viewer_id=cur_viewer['v_id'],
                        twitch_name=cur_viewer['TwitchName'],
                        viewer_type=cur_viewer['Type'],
                        points2=cur_viewer['Points2'],
                        hours=cur_viewer['Hours'],
                        last_seen=cur_viewer['LastSeen'],
                        sub=cur_viewer['Sub']
                    )
                )


if __name__ == '__main__':
    dd = DaveDraw()
    dd.draw()
