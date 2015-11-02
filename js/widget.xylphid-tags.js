function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function htmlEntitiesDecode(str) {
    return String(str).replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');
}

function matchesReferers( elm ){
    self.referers = document.querySelectorAll( '.xylphid-tags > .tag' );
    for (var i=0; i< self.referers.length; i++) {
        if (elm === self.referers[i]) return true;
    }
    return false;
}

/**
 * Sort element chilnodes by value attribute
 */
function sortByValue( elm ) {
    items = elm.childNodes;
    var itemsArr = [];
    for (var i in items) {
        if (items[i].nodeType == 1) { // get rid of the whitespace text nodes
            itemsArr.push(items[i]);
        }
    }

    itemsArr.sort(function(a, b) {
        return a.value == b.value
            ? 0
            : (a.value > b.value ? 1 : -1);
    });

    for (i = 0; i < itemsArr.length; ++i) {
        elm.appendChild(itemsArr[i]);
    }
}

/**
 * Remove tag element parameter
 * Reset and sort datalist options
 */
function remove_tag( elm ) {
    // Get input
    last = elm.parentNode.lastChild;
    while (last !== null && (last.nodeType == 8 || (last.nodeType == 3 && !/\S/.test(last.nodeValue)))) {
        last = last.previousSibling;
    }

    // Create option node
    var option = document.createElement('option');
    option.value = htmlEntitiesDecode(elm.textContent);
    last.list.appendChild(option);

    // Sort options
    sortByValue(last.list);
    elm.remove();
}

/**
 * Bind input :
 *  - Add a new tag if tag name match datalist option
 *  - Remove datalist matched option
 */
function bind_input(event) {
    label = event.target.value;

    // Find matching datalist option
    removable = event.target.list.querySelector('[value="' + label + '"]');
    
    if (removable) {
        // Get id and tag count
        id = event.target.id.replace(/\d+$/, function(x){ return x-1; });
        name = event.target.name.replace(/\d+$/, function(x){ return x-1; });
        nbTags = document.querySelectorAll('[id^="'+id+'"]').length;
        
        // Get related tag id
        value = removable.getAttribute('data-id');
        
        // Create tag
        elm = document.createElement('div');
        elm.classList.add('tag');
        elm.innerHTML = label;

        // Create input
        input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.id = id + '_' + nbTags;
        input.value = value;
        elm.insertBefore(input, elm.firstChild)

        // Clean target value
        event.target.value = '';
        removable.parentNode.removeChild(removable);
        event.target.insertAdjacentHTML('beforebegin', elm.outerHTML);
    }
}

/**
 * Bind keypress for backspace key :
 *  - Remove previous selected tag
 */
function bind_keypress(event) {
    // Remove previous tag
    if (event.keyCode == 8) { // Hit backspace
        parent = event.target.parentNode;
        inputs = parent.querySelectorAll('.tag');
        if (inputs.length) {
            remove_tag( inputs[inputs.length-1] );
        }
    }
}

/**
 * Bind click on tag element :
 *  - Remove clicked tag
 */
function bind_tag_click(event) {
    if (matchesReferers(event.target)) {
        remove_tag( event.target );
    }
}

document.addEventListener('input', bind_input, false);
document.addEventListener('keyup', bind_keypress, false);
document.addEventListener('click', bind_tag_click, false);