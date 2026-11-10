from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Staff
from .models import Assignment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Assignment
from datetime import datetime


@login_required
def dashboard(request):
    # 1. Save new staff member attached specifically to the logged-in manager
    if request.method == 'POST':
        staff_name = request.POST.get('staff_name', '').strip()
        if staff_name:
            Staff.objects.create(name=staff_name, created_by=request.user) # <-- Tagged here!
        return redirect('dashboard')

    # 2. ISOLATION STEP: Only fetch staff members created by this specific user
    search_query = request.GET.get('search', '').strip()
    my_staff = Staff.objects.filter(created_by=request.user) # <-- Filtered here!

    if search_query:
        staff_members = my_staff.filter(name__icontains=search_query).order_by('-created_at')
    else:
        staff_members = my_staff.order_by('-created_at')

    context = {
        'staff_members': staff_members,
        'total_staff': staff_members.count(),
        'search_query': search_query,
    }
    return render(request, 'dashboard.html', context)

@login_required
def staff_profile(request, staff_id):
    # SECURITY GUARD: Ensure a manager can't type a random ID in the URL to view someone else's staff
    staff = get_object_or_404(Staff, id=staff_id, created_by=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        time_given = request.POST.get('time_given') or None
        time_delivered = request.POST.get('time_delivered') or None
        expected_delivery = request.POST.get('expected_delivery') or None
        date_delivered = request.POST.get('date_delivered') or None
        
        # (Keep your existing status assignment calculation logic here...)
        status = 'IN_PROGRESS'
        if title:
            Assignment.objects.create(
                staff=staff, title=title, time_given=time_given, 
                time_delivered=time_delivered, expected_delivery=expected_delivery, 
                date_delivered=date_delivered, status=status
            )
        return redirect('staff_profile', staff_id=staff.id)

    assignments = staff.assignments.all().order_by('-assigned_at')
    context = {
        'staff': staff,
        'assignments': assignments,
        'total_assignments': assignments.count(),
        'on_time': assignments.filter(status='ON_TIME').count(),
        'late_deliveries': assignments.filter(status='LATE').count(),
        'in_progress': assignments.filter(status='IN_PROGRESS').count(),
    }
    return render(request, 'profile.html', context)

@login_required
def delete_staff(request, staff_id):
    if request.method == 'POST':
        # SECURITY GUARD: Only allow deletion if the manager owns this staff profile record
        staff = get_object_or_404(Staff, id=staff_id, created_by=request.user)
        staff.delete()
    return redirect('dashboard')


@login_required
def delete_assignment(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Assignment, id=task_id)
        staff_id = task.staff.id  # Save the staff member's ID before deleting the task
        task.delete()
        return redirect('staff_profile', staff_id=staff_id) # Send them right back to their profile
    return redirect('dashboard')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the new user in automatically after sign-up
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_assignment(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Assignment, id=task_id, staff__created_by=request.user)
        
        # Update details from form inputs
        task.title = request.POST.get('title', '').strip()
        task.time_given = request.POST.get('time_given') or None
        task.time_delivered = request.POST.get('time_delivered') or None
        task.expected_delivery = request.POST.get('expected_delivery') or None
        task.date_delivered = request.POST.get('date_delivered') or None
        
        # Automatically recalculate status based on the updated info
        if task.date_delivered and task.expected_delivery:
            exp_date = datetime.strptime(str(task.expected_delivery), '%Y-%m-%d').date()
            del_date = datetime.strptime(str(task.date_delivered), '%Y-%m-%d').date()
            if del_date > exp_date:
                task.status = 'LATE'
            else:
                task.status = 'ON_TIME'
        elif task.date_delivered:
            task.status = 'ON_TIME'
        else:
            task.status = 'IN_PROGRESS'
            
        if task.title:
            task.save()
            
        return redirect('staff_profile', staff_id=task.staff.id)
    return redirect('dashboard')


