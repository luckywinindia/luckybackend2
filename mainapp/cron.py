from django_cron import CronJobBase, Schedule

from .models import BetEntry, BetWin, ResultSettings
from django.db.models import Count

class BetCron(CronJobBase):
    RUN_EVERY_MINS = 0
    result_settings = ResultSettings.load()
    schedule = Schedule(run_every_mins=result_settings.NextResult)
    code = 'mainapp.my_bet_job'

    def do_game(self, gameID):
        bet_sums = []

        # init the array with zeros...
        for i in range(0,100):
            bet_sums.append(0)
        
        # get new bets that haven't been processed before...
        queryset = BetEntry.objects.filter(isArchive=False, game_id=gameID)
        # calculate sums
        for entry in queryset:
            bet_sums[entry.selected_number] = bet_sums[entry.selected_number] + entry.bet_amount


        least_betted_number = 0
        least_betted_number_score = 0
        i = 0
        # calculate least betted number and archive entry....
        for entry in queryset:
            if i == 0:
                least_betted_number_score = bet_sums[entry.selected_number]
            if bet_sums[entry.selected_number] < least_betted_number_score:
                least_betted_number_score = bet_sums[entry.selected_number]
                least_betted_number = entry.selected_number
            
            entry.isArchive = True
            entry.save()
            i += 1

        least_betted_queryset = BetEntry.objects.filter(selected_number=least_betted_number, game_id=gameID)
        for entry in least_betted_queryset:
            win = BetWin(entry=entry, winner=entry.voter)
            entry.voter.points = entry.voter.points + (entry.bet_amount * 90)
            transaction = Transaction(sender=entry.voter, receiver=entry.voter, amount=entry.bet_amount, transaction_type=3)
            win.save()
            entry.voter.save()
        
        print("GAME {} : least betted number is {} with score of {}".format(gameID, least_betted_number, least_betted_number_score))
    
    def do(self):
        self.do_game(1)
        self.do_game(2)