/*!
* Start Bootstrap - Simple Sidebar v6.0.5 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

 $(document).ready(function(){       
                 $('#consulRegistros').click(function(){      consul_regImg();    })
               
                 $('#consul_ajax').click(function(){      consul_ajax();    })
                 
                  dom();

                  var myModal = new bootstrap.Modal(document.getElementById('exampleModalToggle'), {})

                  

                
 });
       

function dom(){

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

}

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});


function opcion_tablas(mx,pl,sy){
    $('#example').DataTable({
                                        'paging': true,
                                        'lengthChange': true,
                                        'searching': true,
                                        'ordering': true,
                                        'info': true,
                                        'autoWidth': false,
                                        'processing': true,
                                        'scrollY':sy,
                                        'scrollX':true,
                                         max:mx,
                                         pageLength:pl,
                                         lengthMenu:[[5,10,20,-1],[5,10,20,'Todos']],
                                         "order": [],
                                         language: {
                                              "decimal": "",
                                              "emptyTable": "No hay información",
                                              "info": "Mostrando _START_ a _END_ de _TOTAL_ Registros",
                                              "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                                              "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                                              "infoPostFix": "",
                                              "thousands": ",",
                                              "lengthMenu": "Mostrar _MENU_ Registros",
                                              "loadingRecords": "Cargando...",
                                              "processing": "Procesando...",
                                              "search": "Buscar:",
                                              "zeroRecords": "Sin resultados encontrados",
                                              "paginate": {
                                                  "first": "Primero",
                                                  "last": "Ultimo",
                                                  "next": "Siguiente",
                                                  "previous": "Anterior"
                                              }
                                          },
                                      });

}

function mostrarLotImgP(dir){
       $.ajax({
            url:'/lista_imagenes_pro',
            type: 'post',
            data:{dir:dir},
            beforeSend:function(){
            },
            success:function(response){
              
              $("#exampleModalToggle").modal("show");
              $('.modal-body').empty();
              $('.modal-title-img').html("Imagen procesada");

              $('.modal-body').html(response.htmlresponse);
            },
            complete:function(data){
                 $("#exampleModalToggle").modal("hide");
            }
        })
}
function mostrarLotImgO(dir){
       $.ajax({
            url:'/lista_imagenes_ori',
            type: 'post',
            data:{dir:dir},
            beforeSend:function(){
            },
            success:function(response){
              
              $("#exampleModalToggle").modal("show");
              $('.modal-body').empty();
              $('.modal-title-img').html("Imagen fuente");
              $('.modal-body').html(response.htmlresponse);
            },
            complete:function(data){
                 $("#exampleModalToggle").modal("hide");
            }
        })
}

function consul_ajax(){
    valor = "";
    $.ajax({
        url:'/consul_ajax',
        type: 'post',
        data:{valor:valor},
        beforeSend:function(){
            // $("#staticBackdrop").modal("show");
        },
        success:function(response){
           $('.response').empty();
           $('.response').append(response.htmlresponse);
        },
        complete:function(data){
            // $("#staticBackdrop").modal("hide");


        }
    })

}


function consul_regImg(){
    valor = "";
    $.ajax({
        url:'/consul_reg',
        type: 'post',
        data:{valor:valor},
        beforeSend:function(){
            // $("#staticBackdrop").modal("show");
        },
        success:function(response){
          $("#staticBackdrop").modal("hide");
           $('.response').empty();
           $('.response').append(response.htmlresponse);

        },
        complete:function(data){
           opcion_tablas(5,10,410);
             $("#staticBackdrop").modal("hide");


        }
    })
}

function mostrarDatosUs(idelem){
       $.ajax({
            url:'/frm_editUser',
            type: 'post',
            data:{idelem:idelem},
            beforeSend:function(){
            },
            success:function(response){
              
              $("#exampleModalToggle").modal("show");
              $('.modal-body').empty();
              $('.modal-title-img').html("Imagen procesada");

              $('.modal-body').html(response.htmlresponse);
            },
            complete:function(data){
                 $("#exampleModalToggle").modal("hide");
            }
        })
}

function mostrarDatosEl(idelem){
    alert(idelem)
       $.ajax({
            url:'/frm_editElem',
            type: 'post',
            data:{idelem:idelem},
            beforeSend:function(){
            },
            success:function(response){
              
              $("#exampleModalToggle").modal("show");
              $('.modal-body').empty();
              $('.modal-title-img').html("Imagen procesada");

              $('.modal-body').html(response.htmlresponse);
            },
            complete:function(data){
                 $("#exampleModalToggle").modal("hide");
            }
        })
}
