from django.shortcuts import render, redirect
from django.views import View
from .forms import EJPForm
from .models import EJP
from django.conf import settings


class EJPView(View):
    form_class = EJPForm

    def get(self, request):
        user = request.user
        if request.session['beta'] == True and settings.BETA == True and user.is_authenticated and user.id == 6:
            user = request.user
            results = EJP.objects.order_by('-date').all()[:40]

            data = {
                'ejp': results,
            }
            return render(request, 'ejp/index.html', {'form': self.form_class, 'data': data})
        else:
            return redirect('/start/')

    def post(self, request):
        if request.method == 'POST':
            user = request.user
            form = self.form_class(request.POST or None)
            if form.is_valid():
                if not EJP.objects.filter(my=0, date=form.cleaned_data['date']).exists():
                    form.save()

        return redirect('/ejp/')


class Predictions(View):
    def get(self, request):
        user = request.user

        if not request.session['beta']:
            request.session['beta'] = False

        if request.session['beta'] == True and settings.BETA == True and user.is_authenticated and user.id == 6:
            import numpy as np
            from bokeh.plotting import figure
            from bokeh.embed import components
            from .lab.lab import EJPModel

            n = []
            p = []
            y = []
            x_y_pro = []
            y2 = []
            prob = []
            z = []
            x = []
            results = EJP.objects.filter(my=0).all()
            my = EJP.objects.filter(my=1).all()
            count = results.count()
            num_1_50 = count * 5
            num_1_10 = count * 2

            pos_avg = [0, 0, 0, 0, 0]

            for res in results:
                n.append([res.n1, res.n2, res.n3, res.n4, res.n5])
                p.append([res.p1, res.p2])

            for res in my:
                z.append([res.n1, res.n2, res.n3, res.n4, res.n5])
                x.append([res.p1, res.p2])

            z2 = np.array(z)  # my draws 1-50
            x2 = np.array(x)  # my draws 1-10
            n2 = np.array(n)  # results 1-50
            p2 = np.array(p)  # results 1-10
            n_flat = n2.flatten()
            p_flat = p2.flatten()

            for i in range(1, 51, 1):
                y.append(np.count_nonzero(n_flat == i))
                x_y_pro.append(round((y[i - 1] / num_1_50) * 100, 2))
                prob.append(y[i-1] / num_1_50)

            for i in range(1, 11, 1):
                y2.append(np.count_nonzero(p_flat == i))

            # count range of most frequent values 1-10 and so on
            j = 0
            sum = 0
            for i in range(1, 11, 1):
                if i-1 % 10 == 0:
                    pass


            '''1-50 analytics scripts - some more to be added'''
            x_y_pro = np.array(x_y_pro)
            x_y_avg = np.average(x_y_pro)
            # percentage of highest 4 values
            x_y_pro_sorted = np.sort(np.unique(x_y_pro))[-4:]
            # percentage of 2 highest values
            x_y_pro_sorted_highest = np.sort(np.unique(x_y_pro))[-2:]
            pred_avg = np.where(x_y_pro >= x_y_avg)[0]
            # highest than 4th highest number
            prediction_all = np.where(x_y_pro >= x_y_pro_sorted[0])[0]
            # highest than 2nd highest number
            prediction_highest = np.where(x_y_pro >= x_y_pro_sorted_highest[0])[0]
            max_val = np.amax(x_y_pro)
            proc = round((len(pred_avg) / 50) * 100, 0)

            '''percentage of values with range of 10 numbers'''

            rand_5_all = np.sort(np.random.choice(range(1, 51, 1), size=5, replace=False, p=prob))
            rand_5_avg = np.sort(np.random.choice(pred_avg+1, size=5, replace=False))

            unq, cnt = np.unique(n2, axis=0, return_counts=True)
            max_50 = np.max(cnt)
            if max_50 > 1:
                pred_5 = [max_50, unq[cnt == max_50]]
            else:
                pred_5 = [max_50, None]

            '''1-10 analytics scripts'''
            unq, cnt = np.unique(p2, axis=0, return_counts=True)
            pair_max = np.max(cnt)
            if pair_max > 1:
                pair_show = unq[cnt == pair_max]
                pair = [pair_max, pair_show]
            else:
                pair = [pair_max, None]

            plot = figure(title="Numbers occurance (1-50)",
                          sizing_mode="stretch_width",
                          tooltips="@x -> @top")
            plot.vbar(x=range(1, 51, 1), top=y, width=0.4, color="red")
            (div, script) = components(plot)

            plot2 = figure(title="Plus numbers occurance (1-10)",
                           sizing_mode="stretch_width",
                           tooltips="@x -> @top")
            plot2.vbar(x=range(1, 11, 1), top=y2, width=0.7)
            (div2, script2) = components(plot2)

            data = {
                'count': count,
                'proc': proc,
                'prediction_all': prediction_all + 1,
                'prediction_highest': prediction_highest + 1,
                'pred_avg': pred_avg + 1,
                'max_value': max_val,
                'pair': pair,
                'pred_5': pred_5,
                'rand_5_avg': rand_5_avg,
                'rand_5_all': rand_5_all,

            }

            return render(request, 'ejp/predictions.html', {
                'data': data,
                'div': div,
                'div2': div2,
                'script': script,
                'script2': script2,

            })
        else:
            return redirect('/start/')

    def post(self, request):
        pass


class PlusMinus(View):
    def get(self, request):
        data = {}
        user = request.user
        if request.session['beta'] == True and settings.BETA == True and user.is_authenticated and user.id == 6:
            results = EJP.objects.filter(my=1).order_by('-date').all()
            draws = EJP.objects.filter(my=0, date__in=[var.date for var in results]).order_by('-date').all()
            won = 0
            pick_numbers = []
            for var in results:
                for var2 in draws:
                    if var.date == var2.date:
                        pick_numbers.append([var2.n1, var2.n2, var2.n3, var2.n4, var2.n5, var2.p1, var2.p2])

            for var in results:
                won += var.won

            total = 12.5 * results.count()
            income = float(won) - float(total)
            zipped = zip(results, pick_numbers)

            data = {
                'results': zipped,
                'draws': draws,
                'won': won,
                'income': income,
                'total': total,

            }
            return render(request, 'ejp/plus_minus.html', {'data': data})
        else:
            return redirect('/start/')

    def post(self, request):
        pass
