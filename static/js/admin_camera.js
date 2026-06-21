(function () {
  'use strict';

  function ajouterBoutonCamera(input) {
    if (input.dataset.cameraAdded) return;
    input.dataset.cameraAdded = '1';

    var wrapper = document.createElement('div');
    wrapper.style.cssText = 'display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:6px;';

    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);

    var preview = document.createElement('img');
    preview.style.cssText = 'display:none;max-width:120px;max-height:120px;border-radius:8px;border:2px solid #1B3829;object-fit:cover;';
    wrapper.appendChild(preview);

    var btnCamera = document.createElement('button');
    btnCamera.type = 'button';
    btnCamera.innerHTML = '📷 Prendre une photo';
    btnCamera.style.cssText = (
      'background:#1B3829;color:#fff;border:none;padding:7px 16px;'
      + 'border-radius:8px;font-size:.84rem;font-weight:600;cursor:pointer;'
      + 'white-space:nowrap;'
    );
    wrapper.appendChild(btnCamera);

    var inputCamera = document.createElement('input');
    inputCamera.type = 'file';
    inputCamera.accept = 'image/*';
    inputCamera.capture = 'environment';
    inputCamera.style.display = 'none';
    wrapper.appendChild(inputCamera);

    btnCamera.addEventListener('click', function () {
      inputCamera.click();
    });

    function onFileSelected(e) {
      var file = e.target.files[0];
      if (!file) return;

      var dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;

      var reader = new FileReader();
      reader.onload = function (ev) {
        preview.src = ev.target.result;
        preview.style.display = 'block';
      };
      reader.readAsDataURL(file);
    }

    inputCamera.addEventListener('change', onFileSelected);
    input.addEventListener('change', function (e) {
      if (e.target.files[0]) {
        var reader = new FileReader();
        reader.onload = function (ev) {
          preview.src = ev.target.result;
          preview.style.display = 'block';
        };
        reader.readAsDataURL(e.target.files[0]);
      }
    });
  }

  function init() {
    document.querySelectorAll('input[type="file"][name="image"]').forEach(ajouterBoutonCamera);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
