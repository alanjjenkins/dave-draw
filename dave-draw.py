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

class DaveDraw(object):
    def __init__(self):
        self.database_path = 'Viewers3DB.sqlite'
        self.db_conn = sqlite3.connect(self.database_path)

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
                        cur_viewer[16]
                    )
                )

    def display_viewer(self, viewer):
        """
        Outputs the data on all viewers.
        """
        print("""Viewer ID: %s
Twitch Name: %s
Beam Name: %s
Beam ID: %s
Rank: %s
Points: %s
Points2: %s
Hours: %s
Raids: %s
Gains Currency: %s
Gains Hours: %s
InGiveaways: %s
LastSeen: %s
Entrance Message: %s
EntranceMsgType: %s
EntranceSFX: %s"""
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
        return random.choice(self.viewers)
    def display_random_viewer(self):
        self.display_viewer(self.get_random_viewer())

if __name__ == '__main__':
    dd = DaveDraw()
    dd.get_viewers()
    dd.display_random_viewer()
