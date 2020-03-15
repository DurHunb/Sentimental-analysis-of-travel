from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect #重定向
from django.urls import reverse


# 分页导入包
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from ScenicSpot.models import ScenicSpot
from operation.models import ScenicSpotComments


class SpotsView(View):
    """
    景点展示页面
    """
    def get(self, request):
        type = request.GET.get("type", "")
        if type=="":
            all_spots = ScenicSpot.objects.all()
            score = {}
            for spot in all_spots:
                comments = ScenicSpotComments.objects.filter(scenicspot=spot.name)

                for comment in comments:
                    if spot.name not in score:
                        score[spot.name] = comment.Emotional_score
                    else:
                        score[spot.name] += comment.Emotional_score
                score[spot.name] /= len(comments)
            info = []
            # for spot in all_spots:
            #     info.append([
            #         spot,
            #         str(round(score[spot.name], 3)),
            #     ])
            # all_spots = info
            # return render(request, "spots.html", {
            #     'all_spots': all_spots,
            # })
            all_spots1 = []

            while len(all_spots1) != len(all_spots):  # 得分排序
                for spotA in all_spots:
                    if spotA not in all_spots1:
                        spotAscore = score[spotA.name]
                        spotC = spotA

                        for spotB in all_spots:
                            spotBscore = score[spotB.name]
                            if spotB not in all_spots1:

                                if spotBscore >= spotAscore:
                                    spotC = spotB
                                    spotAscore = spotBscore
                                else:
                                    pass
                        all_spots1.append(spotC)

            for spot in all_spots1:
                info.append([spot, str(round(score[spot.name], 3)), ])
            all_spots1 = info
            try:
                page = request.GET.get('page', 1)  # 获取页码
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_spots1, 6, request=request)  # 自带分页器，userblog内的数据，9条数据为一页

            all_spots1 = p.page(page)
            return render(request, "spots.html", {
                'all_spots': all_spots1,
            })

        elif type=="景点":
            all_spots = ScenicSpot.objects.filter(type="景点")
            score = {}
            for spot in all_spots:
                comments = ScenicSpotComments.objects.filter(scenicspot=spot.name)
                for comment in comments:
                    if spot.name not in score:
                        score[spot.name] = comment.Emotional_score
                    else:
                        score[spot.name] += comment.Emotional_score
                score[spot.name] /= len(comments)

            info = []
            all_spots1=[]

            # print(all_spots)
            while len(all_spots1)!=len(all_spots):  #得分排序
                for spotA in all_spots:
                    if spotA not in all_spots1:
                        spotAscore = score[spotA.name]
                        spotC = spotA

                        for spotB in all_spots:
                            spotBscore = score[spotB.name]
                            if spotB not in all_spots1:

                                if spotBscore >= spotAscore:
                                    spotC = spotB
                                    spotAscore = spotBscore
                                else:
                                    pass
                        all_spots1.append(spotC)

            for spot in all_spots1:
                 info.append([spot,str(round(score[spot.name], 3)),])
            all_spots1 = info

            try:
                page = request.GET.get('page', 1)  # 获取页码
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_spots1, 6, request=request)  # 自带分页器，userblog内的数据，9条数据为一页

            all_spots1 = p.page(page)

            return render(request, "spots.html", {
                'all_spots': all_spots1,
            })
        elif type=="酒店":
            all_spots = ScenicSpot.objects.filter(type="酒店")
            score = {}
            for spot in all_spots:
                comments = ScenicSpotComments.objects.filter(scenicspot=spot.name)
                for comment in comments:
                    if spot.name not in score:
                        score[spot.name] = comment.Emotional_score
                    else:
                        score[spot.name] += comment.Emotional_score
                score[spot.name] /= len(comments)
            info = []
            # for spot in all_spots:
            #     info.append([
            #         spot,
            #         str(round(score[spot.name], 3)),
            #     ])
            # all_spots = info
            # return render(request, "spots.html", {
            #     'all_spots': all_spots,
            # })
            all_spots1 = []

            while len(all_spots1) != len(all_spots):  # 得分排序
                for spotA in all_spots:
                    if spotA not in all_spots1:
                        spotAscore = score[spotA.name]
                        spotC = spotA

                        for spotB in all_spots:
                            spotBscore = score[spotB.name]
                            if spotB not in all_spots1:

                                if spotBscore >= spotAscore:
                                    spotC = spotB
                                    spotAscore = spotBscore
                                else:
                                    pass
                        all_spots1.append(spotC)

            for spot in all_spots1:
                info.append([spot, str(round(score[spot.name], 3)), ])
            all_spots1 = info
            try:
                page = request.GET.get('page', 1)  # 获取页码
            except PageNotAnInteger:
                page = 1

            p = Paginator(all_spots1, 6, request=request)  # 自带分页器，userblog内的数据，9条数据为一页

            all_spots1 = p.page(page)
            return render(request, "spots.html", {
                'all_spots': all_spots1,
            })

    # def post(self, request):
    #     all_spots = ScenicSpot.objects.all()
    #     search_keywords = request.POST.get("search", "")
    #     if search_keywords:
    #         all_spots = all_spots.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
    #     return render(request, "spots.html", {
    #         'all_spots': all_spots,
    #         'search': search_keywords,
    #     })


# class SearchCommentsView(View):
#     """
#     搜索评论页面
#     """
#     def post(self, request):
#         spot_comments = ScenicSpotComments.objects.all()
#         search_keywords = request.POST.get("search", "")
#         if search_keywords:
#             spot_comments = spot_comments.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
#         return render(request, "spotcomments.html", {
#             'spot_comments': spot_comments,
#             'search': search_keywords,
#         })


class SpotCommentsView(View):
    """
    景点评论页面
    """
    def get(self, request,spot_name):
        spot_comments = ScenicSpotComments.objects.filter(scenicspot=spot_name).order_by("-Emotional_score")

        scenicspot = ScenicSpot.objects.get(name=spot_name)
        scenicspot.times=scenicspot.times+1
        scenicspot.save()

        count=spot_comments.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(spot_comments, 10, request=request)

        comments = p.page(page)
        return render(request, "spotcomments.html", {
            'spot_comments': comments,
            'spot_name': spot_name,
            'count': count,

        })


    # def post(self, request,spot_name):
    #     spot_comments = ScenicSpotComments.objects.filter(scenicspot=spot_name).order_by("-Emotional_score")
    #     search_keywords = request.POST.get("search", "")
    #     if search_keywords:
    #         spot_comments = spot_comments.filter(comments__contains=search_keywords)
    #     count=spot_comments.count()
    #
    #     # 分页
    #     try:
    #         page = request.GET.get('page', 1)
    #     except PageNotAnInteger:
    #         page = 1
    #
    #     p = Paginator(spot_comments, 10, request=request)
    #
    #     comments = p.page(page)
    #     return HttpResponseRedirect(reverse("spotcomments",kwargs={
    #         'spot_name': spot_name,
    #     }))

        # return render(request, "spotcomments.html", {
        #     'spot_comments': comments,
        #     'keyword':search_keywords,
        #     'spot_name': spot_name,
        #     'count': count,
        # })


class SearchgCommentsView(View):

    def get(self, request,spot_name, keyword):
        spot_comments = ScenicSpotComments.objects.filter(scenicspot=spot_name).order_by("-Emotional_score")

        if keyword:
            spot_comments = spot_comments.filter(comments__contains=keyword)
        count=spot_comments.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(spot_comments, 10, request=request)

        comments = p.page(page)

        return render(request, "spotcomments.html", {
            'spot_comments': comments,
            'keyword':keyword,
            'spot_name': spot_name,
            'count': count,
        })

    def post(self, request, spot_name, keyword):
        keyword=request.POST.get("search", "")
        return HttpResponseRedirect(reverse("searchcomments", kwargs={
            'spot_name': spot_name,
            'keyword': keyword,
        }))

