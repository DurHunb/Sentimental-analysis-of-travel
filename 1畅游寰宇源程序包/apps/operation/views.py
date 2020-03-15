from django.shortcuts import render
from django.views.generic.base import View
import xlrd
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect #重定向
from django.urls import reverse

# Create your views here.
from .forms import UploadExcelForm
from emotion.emotion import sentiment_score,sentiment_score_list
from .models import ScenicSpotComments,UserBlog,UserFavor
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from user.models import UserProfile
from django.contrib import messages

class BlogView(View):
    """
    博客页面
    """
    def get(self, request):
        # try:

            key = request.GET.get("key","")
            if key=='favor':
                if request.user.is_authenticated:
                    blogs = UserFavor.objects.filter(user=request.user)
                    favor = []
                    for blog in blogs:
                        favor.append(UserBlog.objects.get(id=blog.blog_id))
                    try:
                        page = request.GET.get('page', 1)   #获取页码
                    except PageNotAnInteger:
                        page = 1

                    p = Paginator(favor, 9, request=request)   #自带分页器，favor内的数据，9条数据为一页

                    blogs = p.page(page)            #取对象的第page分页对象
                    return render(request, "blog.html", {
                        'blogs': blogs,
                    })
                else:
                    messages.success(request, "请先登录")
                    return render(request, "login.html", {})
            elif key=='own':
                if request.user.is_authenticated:
                    users = UserProfile.objects.filter(username=request.user)
                    print(users)
                    own = []
                    for user in users:
                        all_blog=UserBlog.objects.filter(user_id=user.id)
                        for blog in all_blog:
                            blog=all_blog.get(id=blog.id)
                            own.append(blog)
                    print(own)
                    try:
                        page = request.GET.get('page', 1)  # 获取页码
                    except PageNotAnInteger:
                        page = 1

                    p = Paginator(own, 9, request=request)  # 自带分页器，favor内的数据，9条数据为一页

                    blog = p.page(page)  # 取对象的第page分页对象
                    return render(request, "blog.html", {
                        'blogs': blog,
                    })
                else:
                    messages.success(request, "请先登录")
                    return render(request, "login.html", {})
            else:
                userblog = UserBlog.objects.all().order_by("-add_time")
                # 分页
                try:
                    page = request.GET.get('page', 1)   #获取页码
                except PageNotAnInteger:
                    page = 1

                p = Paginator(userblog, 9, request=request) #自带分页器，userblog内的数据，9条数据为一页

                blogs = p.page(page)
                return render(request, "blog.html", {
                    'blogs': blogs,
                })

        # except:         #出错保险
        #     userblog = UserBlog.objects.all().order_by("-add_time")
        #     # 分页
        #     try:
        #         page = request.GET.get('page', 1)
        #     except PageNotAnInteger:
        #         page = 1
        #
        #     p = Paginator(userblog, 9, request=request)
        #
        #     blogs = p.page(page)
        #     return render(request, "blog.html", {
        #         'blogs':blogs,
        #     })


    def post(self,request):
        # 保存博客
        user=request.user
        title=request.POST.get("title", '')
        image = request.FILES.get("picture")
        desc = request.POST.get("desc", '')
        content = request.POST.get("content", '')
        newblog=UserBlog()
        newblog.user=user
        newblog.title = title
        newblog.image = image
        newblog.desc = desc
        newblog.rich_content = content
        newblog.save()

        return HttpResponseRedirect('/blog/')

class BlogSearchView(View):
    """
    博客搜索页面
    """
    def get(self, request, keyword):
        userblog = UserBlog.objects.all()
        if keyword:
            userblog = userblog.filter(Q(desc__contains=keyword)|Q(title__contains=keyword))
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(userblog, 9, request=request)

        blogs = p.page(page)
        return render(request, "blog.html", {
            'blogs':blogs,
            'keyword': keyword,
        })

    def post(self, request, keyword):
        keyword=request.POST.get("search", "")
        return HttpResponseRedirect(reverse("blogsearch", kwargs={
            'keyword': keyword,
        }))

# class SpotSearchView(View):
#     """
#     景点搜索页面
#     """
#     def get(self, request, keyword):
#         all_spots = ScenicSpot.objects.all()
#         if keyword:
#             userblog = userblog.filter(Q(desc__contains=keyword)|Q(title__contains=keyword))
#         # 分页
#         try:
#             page = request.GET.get('page', 1)
#         except PageNotAnInteger:
#             page = 1
#
#         p = Paginator(userblog, 9, request=request)
#
#         blogs = p.page(page)
#         return render(request, "blog.html", {
#             'blogs':blogs,
#             'keyword': keyword,
#         })
#
#     def post(self, request, keyword):
#         keyword=request.POST.get("search", "")
#         return HttpResponseRedirect(reverse("blogsearch", kwargs={
#             'keyword': keyword,
#         }))

class BlogPublish(View):
    """试图发表博客"""
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, "blogpublish.html", {})
        else:
            messages.success(request, "请先登录")

            return render(request, "login.html", {})

    def post(self,request):
        pass


class UploadExcel(View):
    """
    上传评论信息
    """
    def get(self, request):
        return render(request, "excel.html", {})

    def post(self, request, *args, **kwargs):
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            wb = xlrd.open_workbook(
                filename=None, file_contents=request.FILES['excel'].read())  # 关键点在于这里
        else:
            return render(request, "excel.html", {'msg':"文件格式错误"})
        table = wb.sheets()[0]
        row = table.nrows
        for i in range(1, row):
            try:
                user = table.cell(i, 0).value
                scenicspot = table.cell(i, 1).value
                comments = table.cell(i, 2).value
                #add_time = table.cell(i,3).value
                #province = table.cell(i, 4).value
                #city = table.cell(i, 5).value
                #county = table.cell(i, 6).value

                Emotional_score = sentiment_score(sentiment_score_list(comments))

                ScenicSpotComment = ScenicSpotComments()
                ScenicSpotComment.user=user
                ScenicSpotComment.scenicspot = scenicspot
                ScenicSpotComment.comments = comments
                #ScenicSpotComment.add_time = add_time

                #ScenicSpotComment.province = province
                #ScenicSpotComment.city = city
                #ScenicSpotComment.county = county

                ScenicSpotComment.Emotional_score = Emotional_score
                ScenicSpotComment.save()
            except:
                continue
        return HttpResponseRedirect("http://101.132.46.114:8000/xadmin/ScenicSpot/upload")


class BlogDetails(View):
    """发表博客"""
    def get(self,request,blog_id):
        blog = UserBlog.objects.get(id=blog_id)

        return render(request, "blog-details.html", {
            'blog': blog,
        })

    def post(self,request):
        pass


class Userfavor(View):
    """用户收藏"""
    def get(self, request):
        if request.user.is_authenticated:
            blog_id = request.GET.get("key","")
            if blog_id == "":
                return HttpResponse('错误')
            else:
                userfavor = UserFavor()
                userfavor.user = request.user
                userfavor.blog_id = blog_id
                userfavor.save()

            return HttpResponseRedirect('/blogdetails/{}'.format(blog_id))
        else:
            messages.success(request, "请先登录")
            return render(request, "login.html", {})

class Contact(View):
    def get(self, request):
         return render(request, "contact.html",{})

class Travel(View):
    def get(self, request):
         return render(request, "travel-search.html",{})


from xadmin.views import CommAdminView



