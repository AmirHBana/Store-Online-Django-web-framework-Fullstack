from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from home.models import Product, Category, Comment
from django.contrib import messages
from home.forms import  CommentReplyForm,CommentCreateForm, SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.http import Http404

from django.core.paginator import Paginator
from django.http import Http404

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

class ProductListView(ListView):
    paginate_by = 1
    model = Product
    template_name = 'home/index.html'
    context_object_name = 'products'  # Renamed from 'blog_product'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        form = SearchForm(self.request.GET)
        context['categories'] = categories
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_context_data().get('form')
        if form.is_valid():
            cd = form.cleaned_data['search']
            self.object_list = self.object_list.annotate(similarity=Greatest(
                TrigramSimilarity("name", cd),
                TrigramSimilarity("description", cd),
            )).filter(similarity__gt=0.1).order_by("-similarity")
        
        paginator = Paginator(self.object_list, self.paginate_by)
        page_number = request.GET.get('page')
        last_page = paginator.num_pages
        
        if page_number:
            try:
                page_number = int(page_number)
                if page_number > last_page:
                    page_number = last_page
            except ValueError:
                raise Http404
        
        page_obj = paginator.get_page(page_number)
        context = self.get_context_data(page_obj=page_obj)
        
        return render(request, self.template_name, context)
class ProductDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    template_name = 'home/detail.html'
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Product, slug = kwargs['slug'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request , *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(request, self.template_name, {'product':self.post_instance,'comments':comments, 'form':self.form_class, 'reply_form':self.form_class_reply})
    
    @method_decorator(login_required)
    def post(self, request , *args, **kwargs):
         form = self.form_class(request.POST)
         if form.is_valid():
              new_comment = form.save(commit=False)
              new_comment.user = request.user
              new_comment.product = self.post_instance
              new_comment.save()
              messages.success(request, 'كامنت شما با موفقيت ثبت گرديد', 'success')
              return redirect('home:product_detail', self.post_instance .slug)

	

	
class ProductAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['product_slug'])
        comment = get_object_or_404(Comment, id=kwargs['comment_id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.product = product
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'پاسخ شما با موفقیت ارسال شد.', 'success')
        return redirect('home:product_detail', product.slug)
    
