#!/usr/bin/env python3
import pdb
import random
import sqlite3

class Viewer(object):
    def __init__(self,
        viewer_id,
        twitch_name,
        beam_name,
        beam_id,
        viewer_type,
        rank,
        points,
        points2,
        hours,
        raids,
        gains_currency,
        gains_hours,
        in_giveaways,
        last_seen,
        entrance_message,
        entrance_message_type,
        entrance_sfx
        ):

        self.viewer_id = viewer_id
        self.twitch_name = twitch_name
        self.beam_name = beam_name
        self.beam_id = beam_id
        self.viewer_type = viewer_type
        self.rank = rank
        self.points = points
        self.points2 = points2
        self.hours = hours
        self.raids = raids
        self.gains_currency = gains_currency
        self.gains_hours = gains_hours
        self.in_giveaways = in_giveaways
        self.last_seen = last_seen
        self.entrance_message = entrance_message
        self.entrance_message_type = entrance_message_type
        self.entrance_sfx = entrance_sfx

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
            # skip anyone with no points
            if viewer.points2 == 0:
                next

            ticket_range_beg = latest_ticket + 1
            ticket_range_end = latest_ticket + 1 + viewer.points2
            latest_ticket = ticket_range_end

            viewer.tickets = range(ticket_range_beg, ticket_range_end)

            # assign a range of tickets:
            if self.debug:
                print("Assigning viewer twitch: %s beam: %s tickets %i-%i" % (viewer.twitch_name, viewer.beam_name, viewer.tickets.start, viewer.tickets.stop))
            if ticket_range_beg == ticket_range_end:
                if self.debug:
                    print("Assigning ticket {} to {}".format(ticket_range_beg, viewer.twitch_name))
                self.tickets[ticket_range_beg] = viewer
                next

            for ticket in viewer.tickets:
                if self.debug:
                    print("Assigning ticket {} to {}".format(ticket, viewer.twitch_name))
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

        ticket = random.randint(1, self.total_points)

        try:
            winner = self.tickets[ticket]
        except:
            pdb.set_trace()

        print("\n===== WINNER Twitch: {} / Beam: {} =====\n".format(winner.twitch_name, winner.beam_id))
        print("Picked ticket {}\n".format(ticket))
        print("Winner win chance: {:f}".format(winner.win_chance(self.total_points)))
        print("Winner's ticket range: {}-{}".format(winner.tickets.start, winner.tickets.stop))
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
        print("""Viewer ID: %s\nTwitch Name: %s\nBeam Name: %s\nBeam ID: %s\nRank: %s\nPoints: %s\nPoints2: %s\nHours: %s\nRaids: %s\nGains Currency: %s\nGains Hours: %s\nInGiveaways: %s\nLastSeen: %s\nEntrance Message: %s\nEntranceMsgType: %s\nEntranceSFX: %s"""
            % (
                viewer.viewer_id,
                viewer.twitch_name,
                viewer.beam_name,
                viewer.beam_id,
                viewer.rank,
                viewer.points,
                viewer.points2,
                viewer.hours,
                viewer.raids,
                viewer.gains_currency,
                viewer.gains_hours,
                viewer.in_giveaways,
                viewer.last_seen,
                viewer.entrance_message,
                viewer.entrance_message_type,
                viewer.entrance_sfx
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
        viewers = c.execute('''
                SELECT * FROM Viewer
                WHERE Type != 1
                AND TwitchName NOT IN (
                    \'treeboydave\',
                    \'treebotdave\'
                );
                ''').fetchall()

        self.viewers = []

        for cur_viewer in viewers:
            self.viewers.append(
                    Viewer(
                        cur_viewer[0],
                        cur_viewer[1],
                        cur_viewer[2],
                        cur_viewer[3],
                        cur_viewer[4],
                        cur_viewer[5],
                        cur_viewer[6],
                        cur_viewer[7],
                        cur_viewer[8],
                        cur_viewer[9],
                        cur_viewer[11],
                        cur_viewer[12],
                        cur_viewer[13],
                        cur_viewer[14],
                        cur_viewer[15],
                        cur_viewer[16],
                        cur_viewer[17]
                    )
                )

if __name__ == '__main__':
    dd = DaveDraw()
    dd.draw()
