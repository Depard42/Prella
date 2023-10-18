
isNeedFocus = false; //if true, focus on new table


socketio = io({
    'reconnection': true,
    'reconnectionDelay': 500,
    'maxReconnectionAttempts': Infinity
  })

function clickToEditable(event){
  $(this).attr("contenteditable","true");
  $(this).trigger('focus');
  
}
function focusToEditable(event){
  if (! $(this).hasClass('onedit')){
    var sel = window.getSelection()
    var selected_node = sel.anchorNode
    sel.collapse(selected_node, $(this).text().length)
    $(this).addClass("onedit")
  }
}
function blurEditable(el){
  $(el).removeClass("onedit");
  $(el).attr("contenteditable","false");
}
function keydownEditable(event){
  if (event.key == 'Enter') { 
    $(this).trigger('blur'); 
    event.preventDefault();
  }
}
  
function newTable(id, label){
    const obj = $('<section class="tasks">'+
            ' <h3 class="tasks__title"></h3>'+
            ' <ul class="tasks__list"> </ul>'+
            ' <form class="task-create">'+
            ' <input type="text" size="18" class="inputTaskForm" placeholder="Название карточки" >'+
            ' <input type="submit" class="submitTaskForm" value="Добавить"> </form> </section>',
    ).attr('id', id);
    obj.find('.tasks__title').html(label)
                            .attr("spellcheck", "false")
                            .attr("id", id)
                            .on("blur", function(event){
                                blurEditable(this);
                                t = $(this);
                                socketio.emit('rename table', {id: t.attr('id'),
                                                            label: t.html()});
                                                            console.log($(this).find('.inputTaskForm'))
                                $(this).siblings().find('.inputTaskForm').trigger('focus');
                            })
                            .on('click', clickToEditable)
                            .on('focus', focusToEditable)
                            .on('keydown', keydownEditable)
    obj.appendTo('.panel');
    if (isNeedFocus){
        $('#'+id).ScrollTo({
            duration: 700,
            easing: 'linear'
        });
        if ($('#'+id).find('.tasks__title').text() == '') {
          $('#'+id).find('.tasks__title').trigger('click')
        }
        else {
          $('#'+id).find('.inputTaskForm').trigger('focus');
        }
        isNeedFocus = false;
    }
    obj.find('.tasks__list').attr('id', id);
    Sortable.create(obj.find('.tasks__list').get(0),{
        group: "tasklist-group",
        onStart: function(){
          $('.delete').show();
        },
        onEnd: function(event){
          $('.delete').hide();
          changePosTask(event)},
        delay: 100
    });
    obj.find('.task-create').on("submit", submitNewTaskForm);
};

  function newTask(id, table_id, label){
    const obj = $('<li class="task__item">'+
                 '<p class="item__label"></p></li>')
                 .attr('id',id)
                 .attr('table_id', table_id)
    obj.find('p').html(label).attr("id", id)
                             .attr('table_id', table_id)
                             .attr("spellcheck", "false")
                             .on("blur", function(event){
                                blurEditable(this);
                                t = $(this);
                                socketio.emit('rename task', {id: t.attr('id'),
                                                              table_id: t.attr('table_id'),
                                                              label: t.html()});
                             })
                             .on('click', clickToEditable)
                             .on('focus', focusToEditable)
                             .on('keydown', keydownEditable)
    
    obj.appendTo('.panel #'+table_id+' .tasks__list');
  };

  function addingToDeleteBlock(event){
    //event.preventDefault();
    who = $('.delete').find('section');
    
    if (who.length === 1){
      //table
      id = who.attr('id');
      socketio.emit('del table', {id: id});
    } else {
      //task
      who = $('.delete').find('li');
      id = who.attr('id');
      table_id = who.attr('table_id');
      socketio.emit('del task', {id: id, table_id: table_id});
    };
  
  };
  function changePosTable(ev){
    table_id = $(ev.item).attr('id');
    oldIndex = ev.oldDraggableIndex;
    newIndex = ev.newDraggableIndex;
    if ($(ev.to).attr('id') === "delete"){return 1;};
    if (oldIndex === newIndex){return 1;};
    socketio.emit('change index table', {
      table_id: table_id,
      oldIndex: oldIndex,
      newIndex: newIndex
    });
  };
  function changePosTask(ev){
    task_id = $(ev.item).attr('id');
    toTable = $(ev.to).attr('id');
    fromTable = $(ev.from).attr('id');
    oldIndex = ev.oldDraggableIndex;
    newIndex = ev.newDraggableIndex;
    if (toTable === "delete"){return 1;};
    if (oldIndex === newIndex && fromTable === toTable ){return 1;}
    socketio.emit('change index task', {
      task_id: task_id,
      oldIndex: oldIndex,
      newIndex: newIndex,
      toTable: toTable,
      fromTable: fromTable
    });
  };

  $('.new-table-form').on("submit", function(event){
    event.preventDefault();
    value = $(this).find('.input').val();
    socketio.emit('new table', {
      label: value
    });
    $(this).find('.input').val("");
    isNeedFocus = true;
  });

  function submitNewTaskForm(event){
    event.preventDefault();
    value = $(this).find('.inputTaskForm').val();
    table_id = $(this).parent().attr('id');
    socketio.emit('new task', {
      label: value,
      table_id: table_id
    });
    $(this).find('.inputTaskForm').val('');
  }

  Sortable.create($('.panel').get(0),{
    ghostClass: 'sortable-ghost',
    chosenClass: "sortable-chosen",
    dragClass: "sortable-dragging",
    preventOnFilter: false,
    delay: 100,
    swapThreshold: 2,
    onStart: function(){
      $('.delete').show();
    },
    onEnd: function(event){
      changePosTable(event);
      $('.delete').hide();
    },
    animation: 150,
    easing: " cubic-bezier(0.55, 0, 1, 0.45)",
    filter: 'input',
  });

  Sortable.create($('.delete').get(0),{
    group: {put: true},
    onAdd: addingToDeleteBlock
  });

  socketio.on('create table', create_table);
  function create_table(data){
    newTable(id=data['id'], label=data['label']);
  };
  socketio.on('create task', create_task);
  function create_task(data){
    newTask(id=data['id'], table_id=data['table_id'], label=data['label']);
  };
  socketio.on('delete table', delete_table);
  function delete_table(data){
    $('section#'+data['id']).detach();
  };
  socketio.on('delete task', delete_task);
  function delete_task(data){
    $('li#'+data['id']).detach();
  };
  socketio.on('rename table', rename_table);
  function rename_table(data){
    $('section#'+data['id']+" .tasks__title").html(data['label']);
  };
  socketio.on('rename task', rename_task);
  function rename_task(data){
    $('#'+data['id']+'.item__label').last().html(data['label']);
  };
  socketio.on('change index table', moveTable);
  function moveTable(data){
    table = $('#'+data['table_id']+'.tasks').detach()
    if (data['next'] == 'end'){
      table.appendTo($('.panel'))
    }
    else {
      table.insertBefore($('#'+data['next']+'.tasks'))
    }
  };
  socketio.on('change index task', moveTask);
  function moveTask(data){
    task = $('#'+data['task_id']+'.task__item').detach()
    task.attr('table_id', data['toTable']);
    task.find('p').attr('table_id', data['toTable']);
    if (data['next'] === 'end'){
      task.appendTo($('#'+data['toTable']+'.tasks__list'))
    }
    else{
      task.insertBefore($('#'+data['next']+'.task__item'))
    }
    
  };

  socketio.on('error', errorShow);
  function errorShow(){
    $('#error_mes').css('visibility', 'visible');
  };

  socketio.on('connect', function(){
    $('#status').css('background-color', 'lime');
  });
  socketio.on('disconnect', function(){
    $('#status').css('background-color', 'red');
  });

  /*isScale = false; //if true, user use scale to panel
  $('#scale_button').on('click', () => {
    if (isScale){ // Увеличиваем
      console.log('-')
      $('.panel').css('transform','scale(1) ')
      $('.panel').css('width','100%')
      $('.panel').css('height','calc(100% - 40px)')
      $('#scale_button').html('-')
      isScale = false
    }
    else { // Уменьшаем
      console.log('+')
      $('.panel').css('transform','scale(0.5) translate(-50%, -50%)')
      $('.panel').css('width','200%')
      $('.panel').css('height','calc(200% - 70px)')
      $('#scale_button').html('+')
      isScale = true
    }
  })*/
