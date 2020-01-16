import { TestBed } from '@angular/core/testing';

import { LoginRedirect} from './login-redirect.service';

describe('LoginRedirectService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: LoginRedirect = TestBed.get(LoginRedirect);
    expect(service).toBeTruthy();
  });
});
