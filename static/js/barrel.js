! function (e) {
    var ArrayBarrel = [];
    var barrelArray = $('.barrel');
    if (barrelArray.length > 0) {
        for (let i = 0; i < barrelArray.length; i++) {
            convas_t = $('#' + barrelArray[i].id)
            var canvas = new fabric.Canvas(barrelArray[i].id, {
                selection: false,
                scale: 1,
                moveCursor: 'default',
                hoverCursor: 'default'
            });
            fabric.Object.prototype.selectable = false;

            // БОЧКА №1 //
            var water_up_tanker_1 = new fabric.Circle({
                left: 150,
                top: 100,
                radius: 100,
                scaleY: 0.25,
                originX: 'center',
                originY: 'center',
                fill: '#9DCDFF',
                stroke: '#9DCDFF',
                strokeWidth: 2
            });
            var water_mid_tanker_1 = new fabric.Rect({
                left: 150,
                top: 325,
                width: 200,
                height: 150,
                fill: '#9DCDFF',
                stroke: '#9DCDFF',
                strokeWidth: 2,
                originX: 'center',
                originY: 'center',

            });
            canvas.add(water_mid_tanker_1, water_up_tanker_1);

            // основная бочка #1//
            var circle_tanker_1_1 = new fabric.Circle({
                left: 150,
                top: 100,
                radius: 100,
                fill: 'black',
                scaleY: 0.25,
                originX: 'center',
                originY: 'center'
            });
            var line_tanker_1_1 = new fabric.Line([248, 100, 249, 400], {
                stroke: 'black',
                strokeWidth: 2
            });
            var line_tanker_1_2 = new fabric.Line([50, 100, 49, 400], {
                stroke: 'black',
                strokeWidth: 2
            });
            var circle_tanker_1_2 = new fabric.Circle({
                left: 150,
                top: 400,
                radius: 100,
                scaleY: 0.40,
                originX: 'center',
                originY: 'center',
                startAngle: 0,
                endAngle: 180,
                fill: 'white',
                stroke: 'black',
                strokeWidth: 2
            });
            canvas.add(circle_tanker_1_1, line_tanker_1_1, line_tanker_1_2, circle_tanker_1_2);
            // основная бочка //

            var water_down_tanker_1 = new fabric.Circle({
                left: 150,
                top: 400,
                radius: 98,
                scaleY: 0.40,
                originX: 'center',
                originY: 'center',
                fill: '#9DCDFF',
                stroke: '#9DCDFF',
                strokeWidth: 2
            });
            canvas.add(water_down_tanker_1);

            var water_line_tanker_1 = new fabric.Circle({
                left: 150,
                top: 200,
                radius: 100,
                scaleY: 0.25,
                originX: 'center',
                originY: 'center',
                startAngle: 0,
                endAngle: 180,
                fill: '#9DCDFF',
                stroke: 'black',
                strokeWidth: 2
            });
            canvas.add(water_line_tanker_1);

            var percent_tanker_1 = convas_t.attr("data-value");
            var new_height_water_tanker_1 = water_down_tanker_1.top - (percent_tanker_1 * 3);
            var new_center_water_tanker_1 = water_down_tanker_1.top - (water_down_tanker_1.top - new_height_water_tanker_1) / 2;
            var new_level_water_tanker_1 = water_down_tanker_1.top - new_height_water_tanker_1;

            water_up_tanker_1.set({
                top: new_height_water_tanker_1
            });

            water_mid_tanker_1.set({
                top: new_center_water_tanker_1,
                height: new_level_water_tanker_1
            });

            water_line_tanker_1.set({
                top: new_height_water_tanker_1 + 1
            });

            var text_level_tanker_1 = new fabric.Text(percent_tanker_1.toString(), { left: 130, top: 250, originX: 'center', originY: 'center' });
            var text_percent_tanker_1 = new fabric.Text('  %', { left: percent_tanker_1.toString().length + 180, top: 250, originX: 'center', originY: 'center' });
            canvas.add(text_level_tanker_1, text_percent_tanker_1);
            //canvas.renderAll();
            //ArrayBarrel.push(canvas);
        }

    
 /*
      var canvas = new fabric.Canvas('1_valuecanvas', {
        selection: false,
        scale: 1,
        moveCursor: 'default',
        hoverCursor: 'default'
      });
        console.log(canvas)
      fabric.Object.prototype.selectable = false;
     // БОЧКА №1 //
      var water_up_tanker_1 = new fabric.Circle({
        left: 150,
        top: 100,
        radius: 100,
        scaleY: 0.25,
        originX: 'center',
        originY: 'center',
        fill: '#9DCDFF',
        stroke: '#9DCDFF',
        strokeWidth: 2
      });
      var water_mid_tanker_1 = new fabric.Rect({
        left: 150,
        top: 325,
        width: 200,
        height: 150,
        fill: '#9DCDFF',
        stroke: '#9DCDFF',
        strokeWidth: 2,
        originX: 'center',
        originY: 'center',
    
      });
      canvas.add(water_mid_tanker_1, water_up_tanker_1);

    // основная бочка #1//
      var circle_tanker_1_1 = new fabric.Circle({
        left: 150,
        top: 100,
        radius: 100,
        fill: 'black',
        scaleY: 0.25,
        originX: 'center',
        originY: 'center'
      });
      var line_tanker_1_1 = new fabric.Line([248, 100, 249, 400], {
        stroke: 'black',
        strokeWidth: 2
      });
      var line_tanker_1_2 = new fabric.Line([50, 100, 49, 400], {
        stroke: 'black',
        strokeWidth: 2
      });
      var circle_tanker_1_2 = new fabric.Circle({
        left: 150,
        top: 400,
        radius: 100,
        scaleY: 0.40,
        originX: 'center',
        originY: 'center',
        startAngle: 0,
        endAngle: 180,
        fill: 'white',
        stroke: 'black',
        strokeWidth: 2
      });
      canvas.add(circle_tanker_1_1, line_tanker_1_1, line_tanker_1_2, circle_tanker_1_2);
    // основная бочка //
    
      var water_down_tanker_1 = new fabric.Circle({
        left: 150,
        top: 400,
        radius: 98,
        scaleY: 0.40,
        originX: 'center',
        originY: 'center',
        fill: '#9DCDFF',
        stroke: '#9DCDFF',
        strokeWidth: 2
      });
      canvas.add(water_down_tanker_1);
    
      var water_line_tanker_1 = new fabric.Circle({
        left: 150,
        top: 200,
        radius: 100,
        scaleY: 0.25,
        originX: 'center',
        originY: 'center',
        startAngle: 0,
        endAngle: 180,
        fill: '#9DCDFF',
        stroke: 'black',
        strokeWidth: 2
      });
      canvas.add(water_line_tanker_1);
    
      var percent_tanker_1 = 5;
      var new_height_water_tanker_1 = water_down_tanker_1.top - (percent_tanker_1 * 3);
      var new_center_water_tanker_1 = water_down_tanker_1.top - (water_down_tanker_1.top - new_height_water_tanker_1)/2;
      var new_level_water_tanker_1 = water_down_tanker_1.top - new_height_water_tanker_1;
    
      console.log(new_height_water_tanker_1, new_center_water_tanker_1);
    
      water_up_tanker_1.set({
        top: new_height_water_tanker_1
      });
    
      water_mid_tanker_1.set({
        top: new_center_water_tanker_1,
        height: new_level_water_tanker_1
      });
    
      water_line_tanker_1.set({
        top: new_height_water_tanker_1 + 1
      });
    
      var text_level_tanker_1 = new fabric.Text(percent_tanker_1.toString(), { left: 130, top: 250, originX: 'center', originY: 'center' });
      var text_percent_tanker_1 = new fabric.Text('%', { left: percent_tanker_1.toString().length + 180, top: 250, originX: 'center', originY: 'center' });
      canvas.add(text_level_tanker_1, text_percent_tanker_1);
    */
    

    }

}("undefined" != typeof module ? module.exports : window);