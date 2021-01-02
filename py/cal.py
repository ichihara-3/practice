from datetime import date
import calendar

from flask import Flask


class HTMLCalendarWithToday(calendar.HTMLCalendar):

    def __init__(self, firstweekday=0):
        super().__init__(firstweekday)
        self.today = date.today()

    def update(self):
        self.today = date.today()

    def formatday(self, day, weekday, thismonth=False):
        """
        Return a day as a table cell.
        """
        self.update()
        if day == 0:
            # day outside month
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            if thismonth and day == self.today.day:
                return '<td class="%s" style="color: red"><b>%d</b></td>' % (self.cssclasses[weekday], day)
            else:
                return '<td class="%s">%d</td>' % (self.cssclasses[weekday], day)

    def formatweek(self, theweek, thismonth=False):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, thismonth) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.update()
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, themonth==self.today.month and theyear==self.today.year))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)


app = Flask(__name__)

@app.route('/')
def calendar():
    cal = HTMLCalendarWithToday()
    today = date.today()
    return cal.formatyear(today.year)
