function LinkTo(Tgt) {

  var InA = document.createElement('a');
  InA.setAttribute('href', '#' + Tgt);   // prince bug: foo.href = bar; doesn't work!

  return InA;

}

function TocItem(Tgt) {

  var InLI = document.createElement('li');
  InLI.appendChild(LinkTo(Tgt));

  return InLI;

}

function ToCwalk(Source) {

  var InOL   = document.createElement('ol');
  var DStack = [];

  var Walker = function(lSource) {

    switch (lSource.nodeName.toString().toUpperCase()) {
      case 'H1': if (lSource.getAttribute('notoc') !== 'notoc') { DStack.push({d:1, t:lSource.id}); } break;
      case 'H2': if (lSource.getAttribute('notoc') !== 'notoc') { DStack.push({d:2, t:lSource.id}); } break;
      case 'H3': if (lSource.getAttribute('notoc') !== 'notoc') { DStack.push({d:3, t:lSource.id}); } break;
      case 'H4': if (lSource.getAttribute('notoc') !== 'notoc') { DStack.push({d:4, t:lSource.id}); } break;
      case 'H5': if (lSource.getAttribute('notoc') !== 'notoc') { DStack.push({d:5, t:lSource.id}); } break;
      case 'H6': if (lSource.getAttribute('notoc') !== 'notoc') { DStack.push({d:6, t:lSource.id}); } break;
      default  : break;
    }

    if (lSource.hasChildNodes()) {

      var tNode = lSource.firstChild;
      do {
        Walker(tNode);
      } while (tNode = tNode.nextSibling);

    }

  }

  Walker(Source);

  var curDepth   = 1;
  var curStack   = [InOL];
  var childStack = [];
  var lastChild  = null;

  for (var i=0, iC=DStack.length; i<iC; ++i) {

    var gap = DStack[i].d - curDepth;

    switch (gap) {

      case 0:
        lastChild = TocItem(DStack[i].t)
        curStack[curStack.length-1].appendChild(lastChild);
        break;

      case 1:
        ++curDepth;
        childStack.push(lastChild);
        var newList = document.createElement('ol');
        curStack.push(newList);
        lastChild.appendChild(newList);
        lastChild = TocItem(DStack[i].t)
        curStack[curStack.length-1].appendChild(lastChild);
        break;

      default:
        if (gap > 0) {
          Log.error("Header depth increased by more than one!");
        } else {
          for (z=0; z>gap; --z) {
            --curDepth;
            childStack.pop();
            curStack.pop();
          }
          lastChild = TocItem(DStack[i].t)
          curStack[curStack.length-1].appendChild(lastChild);
        }
        break;

    }


  }

  return InOL;

}

function init() {

  var Body = document.getElementById('bodyid');           // this is what we're scanning

  var ToC  = ToCwalk(Body);                               // make the ToC
  ToC.id   = 'ToCol';                                     // give it an id, for CSS

  document.getElementById('ToCbox').appendChild(ToC);     // put the ToC in place.

}